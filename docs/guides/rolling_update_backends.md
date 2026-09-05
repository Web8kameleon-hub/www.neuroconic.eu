# Rolling Update: `backend`

Use this script to recreate the backend service while checking API health through Nginx.

## Script

- Path: `scripts/rolling_update_backends.ps1`

## Quick Run

```powershell
pwsh -File .\scripts\rolling_update_backends.ps1
```

## Build First

```powershell
pwsh -File .\scripts\rolling_update_backends.ps1 -BuildFirst
```

## Optional Flags

- `-SkipThinkSmoke`: skips `/api/shell/think` smoke request.
- `-HealthTimeoutSeconds 120`: wait longer for health.
- `-PollIntervalSeconds 3`: adjust poll interval.
- `-ComposeFile <path>`: custom compose file location.

## Expected Behavior

- Starts/ensures `backend`, `web`.
- Recreates `backend`, waits for healthy + health endpoint `200`.
- Runs `shell/think` smoke check unless skipped.
- Prints final `docker compose ps` and success message.
