# Giải thích mã nguồn backend

Tài liệu tổng quan theo từng file Python:

- [`backend/__init__.py`](backend/init.md)
- [`backend/config.py`](backend/config.md)
- [`backend/main.py`](backend/main.md)
- [`backend/routes.py`](backend/routes.md)
- [`backend/schemas.py`](backend/schemas.md)
- [`backend/services/__init__.py`](backend/services-init.md)
- [`backend/services/gemini.py`](backend/services-gemini.md)
- [`backend/services/knowledge_base.py`](backend/services-knowledge_base.md)

Backend dùng FastAPI. Lệnh khởi chạy là `uvicorn backend.main:app`; module `main.py` tạo ứng dụng và gắn các route.

## File khởi tạo và cấu hình

### `backend/__init__.py`

Đánh dấu `backend` là Python package để có thể import bằng `backend.routes`, `backend.schemas`.

### `backend/config.py`

- Xác định `ROOT_DIR`, thư mục dữ liệu `DATA_DIR`, nơi lưu vector `VECTOR_DIR`.
- Nạp biến trong `.env`.
- Đặt mặc định cho embedding `intfloat/multilingual-e5-base`, Gemini và danh sách chuyên khoa.
- Muốn chuyển vị trí kho dữ liệu hoặc mô hình, chỉnh `.env.example`/`.env` thay vì sửa logic route.

### `backend/main.py`

Tạo `FastAPI`, đặt tên/phiên bản API, thêm CORS middleware và đăng ký `router` từ `routes.py`. Đây là entry point, không chứa xử lý RAG.

## Request và endpoint

### `backend/schemas.py`

Khai báo các kiểu request Pydantic:

- `Lab`: tên xét nghiệm, giá trị, đơn vị.
- `Case`: tuổi, giới, triệu chứng, tiền sử, xét nghiệm và chuyên khoa.
- `SearchRequest`: câu hỏi, bộ lọc chuyên khoa, số kết quả 1–8.
- `ClinicianFeedback`: ghi chú và thời gian xác nhận.

Các `Field` giới hạn độ dài và phạm vi để FastAPI từ chối request sai trước khi chạy xử lý.

### `backend/routes.py`

Nối HTTP với các dịch vụ:

- `GET /health`: trạng thái API, kho dữ liệu, cấu hình Gemini.
- `GET /documents`: số tệp/đoạn và danh mục tài liệu.
- `POST /ingest`: tùy chọn lưu một file Markdown, rồi lập chỉ mục lại kho.
- `POST /search`: gọi dịch vụ tìm kiếm ngữ nghĩa.
- `POST /analyze`: ghép nội dung ca, tự chọn chuyên khoa nếu cần, truy xuất 5 đoạn, rồi gọi Gemini.
- `POST /feedback`: lưu ghi chú và thời gian vào `data/clinician_feedback.jsonl`, không lưu thông tin ca bệnh.

Route trả HTTP 503 khi dịch vụ embedding, Chroma hoặc Gemini gặp lỗi.

## Dịch vụ

### `backend/services/__init__.py`

Đánh dấu thư mục dịch vụ là package Python.

### `backend/services/knowledge_base.py`

Chịu trách nhiệm về dữ liệu RAG:

- `_parse_frontmatter()` đọc metadata YAML đơn giản ở đầu Markdown.
- `_normalize_specialty()` lấy chuyên khoa chính từ thư mục; metadata có thể chứa tiểu chuyên khoa.
- `_split_document()` chia nội dung theo tiêu đề Markdown và gắn `source`, `section`, `disease`, `specialty`.
- `read_documents()` đọc toàn bộ `.md` trong `DATA_DIR`.
- `document_inventory()` tạo danh mục cho trang quản lý.
- `_get_encoder()` và `_get_collection()` khởi tạo Sentence Transformers/Chroma theo nhu cầu.
- `ingest_documents()` mã hóa đoạn với tiền tố `passage:` và ghi vector vào ChromaDB.
- `ensure_index()` nạp kho lần đầu nếu collection còn trống.
- `search_documents()` mã hóa truy vấn với tiền tố `query:`, lọc chuyên khoa và lấy top-k.

Khi thay cách chia đoạn hoặc metadata, sửa file này. Khi thay cấu trúc collection hoặc embedding, lập chỉ mục lại để tránh trộn vector của mô hình khác.

### `backend/services/gemini.py`

- `case_to_query()` chuyển form ca bệnh thành một câu truy vấn dùng cho RAG.
- `generate_report()` kiểm tra `GOOGLE_API_KEY`, ghép ca với các đoạn nguồn, gửi prompt JSON đến Gemini.
- Sau khi nhận câu trả lời, hàm loại citation ID mà retrieval không trả về.

Prompt yêu cầu mô hình chỉ dùng nguồn truy xuất, không kê đơn, không bịa xác suất và nêu thông tin còn thiếu. Bác sĩ vẫn phải tự đối chiếu nguồn.
