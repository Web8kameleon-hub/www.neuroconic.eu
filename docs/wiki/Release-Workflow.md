# Release Workflow

## Standard Flow

1. Finalize code + tests
2. Update `CHANGELOG.md`
3. Commit to `main`
4. Push to `origin`
5. Create semantic tag (`vX.Y.Z`)
6. Publish GitHub release notes

## Minimum Release Checklist

- [ ] Working tree clean
- [ ] Focused tests passed
- [ ] Changelog includes new version
- [ ] Tag points to intended commit
- [ ] Release URL verified

## Rollback Rule

Nëse release ka regresion kritik:

- krijo hotfix branch,
- rregullo root cause,
- publiko patch release të ri.
