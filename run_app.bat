@echo off
setlocal
cd /d "%~dp0"
py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 (
  echo Signal Hub needs Python 3.10 or newer.
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
  echo Creating Signal Hub's private Python environment...
  py -m venv .venv
)
".venv\Scripts\python.exe" -c "import streamlit, yaml, tracksignal" >nul 2>&1
if errorlevel 1 (
  echo Installing Signal Hub's open-source packages...
  ".venv\Scripts\python.exe" -m pip --disable-pip-version-check install --prefer-binary -r requirements.txt
  if errorlevel 1 (
    pause
    exit /b 1
  )
)
if "%SIGNALHUB_PORT%"=="" set SIGNALHUB_PORT=8610
if "%SIGNALHUB_MAX_UPLOAD_MB%"=="" set SIGNALHUB_MAX_UPLOAD_MB=10000
echo Starting Signal Hub at http://127.0.0.1:%SIGNALHUB_PORT% ...
".venv\Scripts\python.exe" -m streamlit run hub/app.py --server.headless=true --server.address=127.0.0.1 --server.port=%SIGNALHUB_PORT% --server.maxUploadSize=%SIGNALHUB_MAX_UPLOAD_MB% --server.fileWatcherType=none --browser.gatherUsageStats=false
if errorlevel 1 pause
