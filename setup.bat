@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================================
echo   Yushan's Efficiency Site - One-click Setup
echo   (double-click to run; needs internet for first setup)
echo ============================================================
echo.

REM ---- resolve python ----
set PY=
where python >nul 2>nul && set PY=python
if not defined PY (where py >nul 2>nul && set PY=py)
if not defined PY (
    echo [FAIL] Python not found.
    echo        Install Python 3.10+ from https://python.org
    echo        and check "Add Python to PATH" during install.
    pause
    exit /b 1
)
echo [OK] Using Python: %PY%

REM ---- 1. check / install Ollama ----
where ollama >nul 2>nul
if %errorlevel%==0 (
    echo [OK] Ollama already installed
    goto :pull
)

echo [1/4] Installing Ollama via winget (to D:\Ollama, ~100MB, needs internet)...
winget install -e --id Ollama.Ollama --location "D:\Ollama" --accept-package-agreements --accept-source-agreements
if %errorlevel%==0 (
    echo [OK] Ollama installed to D:\Ollama.
    set "PATH=D:\Ollama;%PATH%"
    timeout /t 3 >nul
) else (
    echo [WARN] Could not install to D:\Ollama (winget --location unsupported?).
    echo        Trying default install location on C:...
    winget install -e --id Ollama.Ollama --accept-package-agreements --accept-source-agreements
    if %errorlevel%==0 (
        echo [OK] Ollama installed (default location).
        set "PATH=%LOCALAPPDATA%\Programs\Ollama;%PATH%"
        timeout /t 3 >nul
    ) else (
        echo [FAIL] winget install failed.
        echo        Download Ollama manually from https://ollama.com
        echo        then run this script again.
        pause
        exit /b 1
    )
)

:pull
REM ---- redirect model storage to D: (keep C: system disk clean) ----
set "OLLAMA_MODELS=D:\OllamaModels"
setx OLLAMA_MODELS "D:\OllamaModels" >nul 2>nul
echo       Model will be stored at D:\OllamaModels
REM ---- 2. pull model ----
echo [2/4] Pulling model qwen2.5:7b (~4.7GB, depends on network)...
ollama pull qwen2.5:7b
if %errorlevel%==0 (echo [OK] Model pulled) else (echo [WARN] Model pull failed; run 'ollama pull qwen2.5:7b' later)

REM ---- 3. venv + deps ----
echo [3/4] Creating venv and installing deps (Flask + ollama)...
%PY% -m venv .venv
if %errorlevel%==0 (
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if %errorlevel%==0 (echo [OK] Dependencies installed) else (echo [WARN] Deps install failed)
) else (
    echo [WARN] venv failed; trying global install...
    %PY% -m pip install -r requirements.txt
)

REM ---- 4. start ----
echo [4/4] Starting the website...
echo       Open  http://127.0.0.1:5000  in your browser
echo       Press  Ctrl+C  to stop the server
python app.py
