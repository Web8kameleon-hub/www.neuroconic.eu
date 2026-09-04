# Production Autodeploy

The workflow [deploy-production.yml](../../.github/workflows/deploy-production.yml)
deploys only after the `Neurosonic CI - Zero Fake Enforcement` workflow succeeds
on `main`. It uses the exact commit SHA evaluated by CI and starts the existing
Docker Compose stack on the deployment host.

Autodeploy is disabled by default. Set the repository or production-environment
variable `DEPLOY_ENABLED` to `true` only after configuring the target.

## Required configuration

Create a GitHub `production` environment with any required approval rules, then
add these environment secrets:

- `DEPLOY_HOST`: hostname or IP address of the server.
- `DEPLOY_USER`: non-root SSH user permitted to manage the deployment checkout.
- `DEPLOY_SSH_KEY`: private SSH key for that user.

Add this environment variable:

- `DEPLOY_PATH`: absolute path of the existing Git checkout on the server.

The host must already have Git, Docker Engine, Docker Compose, and the project
checkout. The workflow verifies `/api/health` inside the backend container after
Compose completes.

## Safety properties

- A failed CI run cannot trigger a production deploy.
- The workflow deploys a detached, verified commit SHA rather than an arbitrary
  remote branch head.
- Deployments are serialized with the `production-deploy` concurrency group.
- SSH host keys are recorded before the connection and deployment secrets are
  supplied only as environment variables.

To disable deployment immediately, set `DEPLOY_ENABLED` to any value other than
`true` or remove the production environment secrets.
