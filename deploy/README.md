# Deploying Signal Hub

Hand-off for hosting. DNS, reverse proxy, TLS and firewall are set up on the server, not in this repo.

| | |
|---|---|
| Image | `ghcr.io/ulrikerlingsen/signal-hub` (built by `.github/workflows/image.yml` on pushes to `main` and `v*` tags) |
| Container port | `8501` (HTTP, Streamlit; needs WebSocket upgrade on the proxy for `/_stcore/stream`) |
| Health check | `GET /_stcore/health` returns `ok` |
| Environment variables | none required. The image defaults to a public demo: `SIGNAL_PUBLIC=1` (every tool applies its demo limits) and `STREAMLIT_SERVER_MAX_UPLOAD_SIZE=50`. For an internal company deployment set `SIGNAL_PUBLIC=0` and a larger `STREAMLIT_SERVER_MAX_UPLOAD_SIZE` (e.g. 10000). Optional: `SIGNALHUB_DEBUG=1` shows tracebacks in error cards (do not use in public) |
| User | non-root (`uid 10001`) |
| Disk | none written at runtime; no volume needed |
| Memory | plan for about 1.5–2 GB: one Python process holds every tool's libraries (pandas, scipy, scikit-learn, statsmodels, plotly) plus per-session data. Uploads are capped at 50 MB per file by default. For an internal company deployment with large files, budget roughly 3–5× the largest file per concurrent analysis on top of the base. |
| CPU | 1–2 vCPU is enough for a demo; heavy analyses run in the visitor's session thread |
| Suggested host name | `signal.ulrikerlingsen.com` |

Run it:

```bash
docker run -d --name signal-hub --restart unless-stopped -p 127.0.0.1:8501:8501 ghcr.io/ulrikerlingsen/signal-hub:main
```

The proxy must forward WebSocket upgrades (Streamlit uses `/_stcore/stream`). Example for Caddy:

```
signal.ulrikerlingsen.com {
    reverse_proxy 127.0.0.1:8501
}
```

To update a tool: bump its `tag:` in `apps.yaml`, run `python scripts/gen_requirements.py`, push; the image workflow
builds a new image; pull and restart the container.
