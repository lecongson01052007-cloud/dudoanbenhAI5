if (-not (Test-Path .venv)) { python -m venv .venv }
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$root = (Get-Location).Path
$backendLog = Join-Path $root 'backend.log'
$backendError = Join-Path $root 'backend-error.log'
Start-Process -FilePath '.\.venv\Scripts\python.exe' -ArgumentList '-m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000' -WorkingDirectory $root -WindowStyle Hidden -RedirectStandardOutput $backendLog -RedirectStandardError $backendError
& .\.venv\Scripts\python.exe -m streamlit run frontend/streamlit_app.py --server.headless true --server.address 127.0.0.1 --server.port 8501 --browser.gatherUsageStats false
