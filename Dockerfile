FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    ARROW_DEFAULT_MEMORY_POOL=system

WORKDIR /app
# Apps are pinned to release-tag archives in requirements-apps.txt (generated from apps.yaml); no git client needed.
COPY requirements.txt requirements-apps.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY .streamlit ./.streamlit
COPY apps.yaml ./
COPY hub ./hub
COPY signal-theme/signal_theme.py signal-theme/signal_font.py ./signal-theme/
COPY signal-theme/assets/marks ./signal-theme/assets/marks
RUN useradd --create-home --uid 10001 signalhub
USER signalhub

EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"
CMD ["python", "-m", "streamlit", "run", "hub/app.py", "--server.headless=true", "--server.address=0.0.0.0", "--server.port=8501", "--server.maxUploadSize=50", "--server.fileWatcherType=none", "--client.showErrorDetails=none", "--browser.gatherUsageStats=false"]
