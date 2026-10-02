@echo off
setlocal
cd /d "%~dp0"
py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 (
  echo {{Name}} needs Python 3.10 or newer.
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
  echo Creating {{Name}}'s private Python environment...
  py -m venv .venv
)
".venv\Scripts\python.exe" -c "import streamlit, defusedxml" >nul 2>&1
if errorlevel 1 (
  echo Installing {{Name}}'s open-source packages...
  ".venv\Scripts\python.exe" -m pip --disable-pip-version-check install --prefer-binary -r requirements.txt
  if errorlevel 1 (
    pause
    exit /b 1
  )
)
if "%{{ENV}}_PORT%"=="" set {{ENV}}_PORT={{port}}
echo Starting {{Name}} at http://127.0.0.1:%{{ENV}}_PORT% ...
".venv\Scripts\python.exe" -m streamlit run app.py --server.headless=true --server.address=127.0.0.1 --server.port=%{{ENV}}_PORT% --server.maxUploadSize={{max_upload_mb}} --server.fileWatcherType=none --browser.gatherUsageStats=false
if errorlevel 1 pause
