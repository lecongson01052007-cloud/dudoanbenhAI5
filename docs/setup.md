# Cài đặt và chạy trên Windows

## Thiết lập một lần

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Mở `.env`, điền khóa Google AI Studio vào `GOOGLE_API_KEY=`. Không commit tệp `.env` hoặc chia sẻ khóa.

## Chạy API và giao diện riêng

Mở hai cửa sổ PowerShell tại thư mục dự án.

API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Giao diện:

```powershell
.\.venv\Scripts\python.exe -m streamlit run frontend/streamlit_app.py
```

Hoặc chạy `.\run.ps1`; script khởi động API nền và chạy Streamlit.

## Địa chỉ

- Giao diện: `http://127.0.0.1:8501`
- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`

Lần đầu truy vấn, Sentence Transformers tải `intfloat/multilingual-e5-base`. Các vector sau đó được giữ trong `vector_db/`. Nếu sửa `.env`, hãy khởi động lại API để đọc lại cấu hình.
