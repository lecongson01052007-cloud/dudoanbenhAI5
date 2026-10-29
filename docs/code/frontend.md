# Giải thích mã nguồn giao diện

## `frontend/streamlit_app.py`

Đây là entry point của Streamlit và chứa ba trang dùng chung trong một ứng dụng.

### Khởi tạo

- Nạp `.env` ở thư mục gốc dự án.
- Đọc `API_URL`, mặc định `http://localhost:8000`.
- Thiết lập tiêu đề, bố cục và CSS.
- Sidebar hiển thị trạng thái backend, số tài liệu và cảnh báo khi chưa cấu hình khóa Gemini.

### Hàm giao diện

- `api_get()` và `api_post()` gửi request tới FastAPI.
- `header()` tạo phần tiêu đề cho từng trang.
- `citation_card()` hiển thị mã nguồn, chuyên khoa, độ phù hợp và nội dung đoạn trích.

### Ba trang

1. **Phân tích ca bệnh**: form tuổi/giới, triệu chứng, tiền sử, xét nghiệm; gửi `POST /analyze`; hiển thị nhận định, mức khẩn, chẩn đoán phân biệt, nguồn và form ghi chú bác sĩ.
2. **Tra cứu kho tri thức**: gửi câu hỏi/chuyên khoa/top-k tới `POST /search`; mở rộng từng kết quả để đọc trích đoạn.
3. **Quản lý tài liệu**: lấy danh mục từ `GET /documents`, tải Markdown hoặc yêu cầu lập chỉ mục qua `POST /ingest`.

Muốn đổi trường nhập hoặc cách trình bày kết quả, sửa trang tương ứng trong file này. Kiểu dữ liệu API vẫn cần khớp với `backend/schemas.py`.

## `frontend/README.md`

Hướng dẫn ngắn cho thư mục giao diện; không phải file chạy ứng dụng.
