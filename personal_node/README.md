# Personal Node UI Composer

This folder contains local-first assets for user-created personal dashboards.

## What it provides

- `ui_composer.html`: local UI builder page for creating personal panel schemas.
- `profiles/*.json`: generated panel profiles saved on the user's machine.

## Backend endpoints

- `POST /api/ui/design` generate a schema from prompt + preferences and optionally save.
- `GET /api/ui/panels` list saved profiles.
- `GET /api/ui/panels/{profile_id}` load one profile.
- `POST /api/ui/panels/{profile_id}` save a panel payload manually.

## Open locally

Use the backend route:

- `http://127.0.0.1:8000/ui-composer`
