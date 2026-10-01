## Purpose

Describe what this change does for a visitor or a maintainer.

## Boundaries checked

- [ ] No analysis logic, data processing or storage was added to the Hub.
- [ ] Apps are listed only in `apps.yaml`; requirement files were regenerated.
- [ ] Design changes were made in `signal-theme/` (and synced), not in an app copy.
- [ ] The front page makes no traction or user claims.

## Verification

- [ ] Tests pass (`python -m pytest`).
- [ ] Ruff passes.
- [ ] Documentation and STATUS are updated.
