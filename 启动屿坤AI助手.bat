@echo off
cd /d "C:\Users\XIAYULUN\WorkBuddy\2026-10-22-16-34-08\project-a-website"
if exist launcher_error.log del launcher_error.log
echo Starting AI Assistant (Ollama + Flask + browser)...
"C:\Users\XIAYULUN\WorkBuddy\2026-10-22-16-34-08\project-a-website\.venv\Scripts\python.exe" launcher.py
echo.
echo Exited with code %errorlevel%
pause
