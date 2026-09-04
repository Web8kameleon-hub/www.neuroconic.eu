# Personal Node UI Composer

This folder contains local-first assets for user-created personal dashboards.

## What it provides

- `ui_composer_dynamic.html`: local UI builder page for creating personal panel schemas.
- `profiles/*.json`: generated panel profiles saved on the user's machine.

## Backend endpoints

- `POST /api/ui/chat` conversational endpoint: send a free-form message
  (no JSON/preferences needed), get back a human reply plus the generated
  panel schema. Powers the chat-first experience in
  `ui_composer_dynamic.html` for non-technical users.
- `POST /api/ui/design` generate a schema from prompt + preferences and optionally save.
- `GET /api/ui/panels` list saved profiles.
- `GET /api/ui/panels/{profile_id}` load one profile.
- `POST /api/ui/panels/{profile_id}` save a panel payload manually.
- `GET /api/ui/plugins/{profile_id}` list dynamic plugins for a user profile.
- `POST /api/ui/plugins/{profile_id}` attach plugin by any address (website/email/app/internal/local) with liability acknowledgment.

## Open locally

Use the backend route:

- `http://127.0.0.1:8000/ui-composer`
