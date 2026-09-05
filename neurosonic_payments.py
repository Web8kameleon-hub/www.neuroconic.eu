#!/usr/bin/env python3
"""Neurosonic Payments: Stripe Checkout + webhook për "1-Day Unlimited Access".

Modeli: pagesë e vetme (one-time) prej 1 EUR që aktivizon entitlement për
24 orë. Nuk përdor abonime recurring — çdo akses i ri kërkon një pagesë
të re (checkout session e re).

Ky modul lidh Stripe me `neurosonic_auth.NeurosonicAuth`: pas një pagese
të suksesshme (webhook `checkout.session.completed`), entitlement-i i
përdoruesit përditësohet me kohën e skadimit (now + 24h).

Kërkon variablat e mjedisit:
    STRIPE_SECRET_KEY      - çelësi sekret i Stripe (sk_live_... / sk_test_...)
    STRIPE_WEBHOOK_SECRET  - sekreti i endpoint-it webhook (whsec_...)
    STRIPE_PRICE_ID        - ID e price-it "One-off" 1 EUR (price_...)
    STRIPE_SUCCESS_URL     - URL ku ridrejtohet përdoruesi pas pagesës
    STRIPE_CANCEL_URL      - URL ku ridrejtohet nëse anulon
"""

from __future__ import annotations

import os
import time
from typing import Any

import stripe

ENTITLEMENT_DURATION_SECONDS = 24 * 60 * 60  # 24 orë


class PaymentsError(Exception):
    """Gabim gjatë krijimit të checkout session ose verifikimit të webhook."""


class NeurosonicPayments:
    """Krijon Stripe Checkout sessions dhe verifikon webhooks për 1-day pass."""

    def __init__(self, auth: Any):
        self._auth = auth  # NeurosonicAuth instance, injektuar për të shmangur cikël importi
        stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")

    @property
    def _price_id(self) -> str:
        price_id = os.environ.get("STRIPE_PRICE_ID", "")
        if not price_id:
            raise PaymentsError("STRIPE_PRICE_ID nuk është konfiguruar")
        return price_id

    @property
    def _webhook_secret(self) -> str:
        secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
        if not secret:
            raise PaymentsError("STRIPE_WEBHOOK_SECRET nuk është konfiguruar")
        return secret

    def create_checkout_session(self, email: str) -> dict[str, Any]:
        """Krijon një Checkout Session one-time prej 1 EUR për `email`."""
        if not stripe.api_key:
            raise PaymentsError("STRIPE_SECRET_KEY nuk është konfiguruar")

        success_url = os.environ.get(
            "STRIPE_SUCCESS_URL", "https://www.neurosonic.eu/dashboard?paid=1"
        )
        cancel_url = os.environ.get(
            "STRIPE_CANCEL_URL", "https://www.neurosonic.eu/pricing"
        )

        try:
            session = stripe.checkout.Session.create(
                mode="payment",  # one-time, JO "subscription"
                payment_method_types=["card"],
                line_items=[{"price": self._price_id, "quantity": 1}],
                customer_email=email,
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={"neurosonic_email": email, "product": "1day_unlimited"},
            )
        except stripe.StripeError as exc:
            raise PaymentsError(f"Stripe checkout dështoi: {exc}") from exc

        return {"checkout_url": session.url, "session_id": session.id}

    def handle_webhook(self, payload: bytes, signature_header: str) -> dict[str, Any]:
        """Verifikon nënshkrimin e webhook-ut dhe aktivizon entitlement nëse pagesa u krye."""
        try:
            event = stripe.Webhook.construct_event(
                payload, signature_header, self._webhook_secret
            )
        except ValueError as exc:
            raise PaymentsError("Payload i pavlefshëm") from exc
        except stripe.SignatureVerificationError as exc:
            raise PaymentsError("Nënshkrim i pavlefshëm") from exc

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            email = (session.get("customer_email") or "").strip().lower()
            if not email:
                metadata = session.get("metadata") or {}
                email = (metadata.get("neurosonic_email") or "").strip().lower()

            if email:
                now = time.time()
                entitlement = {
                    "tier": "unlimited",
                    "activated_at": now,
                    "expires_at": now + ENTITLEMENT_DURATION_SECONDS,
                    "stripe_session_id": session.get("id"),
                    "amount_total": session.get("amount_total"),
                    "currency": session.get("currency"),
                }
                self._auth.set_entitlement(email, entitlement)
                return {"status": "activated", "email": email}

            return {"status": "no_email_found"}

        return {"status": "ignored", "event_type": event["type"]}


def is_entitlement_active(entitlement: dict[str, Any] | None) -> bool:
    """Kontrollon nëse entitlement-i ekziston dhe s'ka skaduar ende."""
    if not entitlement:
        return False
    return entitlement.get("expires_at", 0) > time.time()
