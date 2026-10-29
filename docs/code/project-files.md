# Giải thích cấu hình và file khởi chạy

## `run.ps1`

Script PowerShell để bắt đầu dự án:

1. Tạo `.venv` nếu chưa có.
2. Cài các thư viện từ `requirements.txt`.
3. Khởi chạy FastAPI nền tại `127.0.0.1:8000`, log vào `backend.log` và `backend-error.log`.
4. Chạy Streamlit tại `127.0.0.1:8501` ở cửa sổ hiện tại.

Script cần được chạy từ thư mục gốc dự án. Khi đóng tiến trình Streamlit, API nền có thể vẫn chạy; dừng API bằng cách tìm tiến trình Python đang lắng nghe cổng 8000 hoặc khởi động lại máy.

## `requirements.txt`

Khai báo thư viện:

- `fastapi`, `uvicorn`: API và server.
- `streamlit`: giao diện.
- `sentence-transformers`, `chromadb`: embedding và vector store.
- `google-genai`: Gemini.
- `pydantic`, `python-multipart`, `python-dotenv`: validate request, upload và cấu hình.
- `pandas`, `openpyxl`: bảng dữ liệu giao diện và hỗ trợ file Excel.

Các phiên bản được giới hạn theo khoảng để tránh tự cập nhật sang major version không tương thích.

## `.env.example`

Mẫu biến môi trường. Sao chép thành `.env` rồi tự điền khóa Gemini. Các biến đường dẫn/model có giá trị mặc định:

- `GOOGLE_API_KEY`: khóa dịch vụ Gemini; giữ bí mật.
- `GEMINI_MODEL`: tên model tạo báo cáo.
- `EMBEDDING_MODEL`: model embedding local.
- `DATA_DIR`, `VECTOR_DIR`: thư mục tài liệu và chỉ mục.
- `API_URL`: địa chỉ backend mà Streamlit gọi.

`.env` bị Git bỏ qua; không ghi khóa thật vào tài liệu hoặc commit.
