@echo off
if exist ".\_python_\" (
    call ".\_python_\Scripts\activate.bat"
) else (
    python -m venv _python_
    call ".\_python_\Scripts\activate.bat"
    ".\_python_\Scripts\python.exe" -m pip install --upgrade pip
    ".\_python_\Scripts\pip.exe" install --no-input -r requirements.txt
)
".\_python_\Scripts\python.exe" ".\main.py"
call deactivate
pause
exit