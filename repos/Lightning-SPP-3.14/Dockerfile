# =============================================================================
# LIGHTNING SPP 3.14 - Docker Image zyrtar
# Scan -> Process -> Print Engine
# Nga Neurosonic / Clisonix Trinity+ASI Ecosystem
# =============================================================================

FROM python:3.11-slim

LABEL maintainer="Neurosonic <clisonix@pm.me>"
LABEL vendor="Clisonix / ABA GmbH"
LABEL version="3.14"
LABEL description="Lightning SPP 3.14 - Scan -> Process -> Print Engine"

# =============================================================================
# SISTEMI
# =============================================================================

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV LIGHTNING_SPP_VERSION=3.14
ENV LIGHTNING_SPP_PORT=8080
ENV LIGHTNING_SPP_HOST=0.0.0.0
ENV LIGHTNING_SPP_MODE=production
ENV ZERO_FAKE=true
ENV ZERO_DEPENDENCIES=true

WORKDIR /app

# =============================================================================
# INSTALIMI I MODULEVE THEMELORE
# =============================================================================

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# SKEDARET E LIGHTNING SPP 3.14
# =============================================================================

COPY . .

# =============================================================================
# NEUROSONIC BRIDGE - Lidhje me ekosistemin
# =============================================================================

RUN mkdir -p /app/bridge /app/memory /app/logs

# =============================================================================
# PORTA
# =============================================================================

EXPOSE 8080

# =============================================================================
# KOMANDA E NISJES
# =============================================================================

CMD ["python", "lightning_spp_server.py"]
