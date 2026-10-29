# `backend/config.py`

## Vai trò

Tập trung các đường dẫn và thiết lập dùng chung cho API, kho tài liệu và dịch vụ RAG.

## Thành phần chính

- `ROOT_DIR`: thư mục gốc dự án, suy ra từ vị trí file.
- `load_dotenv(...)`: đọc biến cấu hình từ `.env` ở thư mục gốc.
- `DATA_DIR`, `VECTOR_DIR`: đường dẫn kho Markdown và cơ sở dữ liệu vector; có thể ghi đè bằng biến môi trường cùng tên.
- `EMBEDDING_MODEL`, `GEMINI_MODEL`: tên mô hình mặc định, có thể ghi đè qua môi trường.
- `SPECIALTIES`, `ALL_SPECIALTIES`, `CASE_SPECIALTIES`: danh sách chuyên khoa dùng trong API và giao diện.

Các module route và dịch vụ lấy cấu hình chung tại đây. Khóa Gemini được đọc riêng từ `GOOGLE_API_KEY`.
