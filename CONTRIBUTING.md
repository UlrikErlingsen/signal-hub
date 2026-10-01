# Contributing

Signal Hub assembles released Signal tools. Contributions should keep it that way:

- No business logic, data processing or shared storage in the Hub. A change to a tool happens in that tool's
  repository, as a release, and reaches the Hub through its `tag:` in `apps.yaml`.
- `apps.yaml` is the only list of apps. After editing it, run `python scripts/gen_requirements.py`.
- Design changes go in `signal-theme/`, then `python scripts/sync_theme.py` copies them into the app clones.
- Keep the front page honest: no traction or user claims, and say that the suite is built with AI-assisted
  development.

Before submitting a change:

```bash
python -m pytest
python -m ruff check .
```

Use fictional data only. Do not contribute proprietary material without clear redistribution rights.
