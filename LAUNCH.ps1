Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
if (Test-Path ".\_python_" -PathType Container){
	& .\_python_\Scripts\Activate.ps1
} else {
	python -m venv _python_
	& .\_python_\Scripts\Activate.ps1
	.\_python_\Scripts\python.exe -m pip install --upgrade pip
	.\_python_\Scripts\pip.exe install --no-input -r requirements.txt
}
.\_python_\Scripts\python.exe .\main.py
deactivate