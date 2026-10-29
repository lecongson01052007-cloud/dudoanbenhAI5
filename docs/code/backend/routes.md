# `backend/routes.py`

## Vai trò

Khai báo HTTP endpoint của backend và điều phối request tới schema cùng dịch vụ tương ứng.

## Endpoint

- `GET /health`: trả trạng thái, danh sách chuyên khoa, trạng thái thư mục dữ liệu và việc đã cấu hình `GOOGLE_API_KEY` hay chưa.
- `GET /documents`: trả danh mục tài liệu và số lượng chunk từ `document_inventory()`.
- `POST /ingest`: tùy chọn nhận file `.md` tối đa 5 MB, lưu vào `DATA_DIR/uploaded`, đọc kho Markdown rồi lập chỉ mục lại. Kiểm tra loại file và kích thước trả mã 400 hoặc 413.
- `POST /search`: nhận `SearchRequest`, gọi `search_documents()` với truy vấn, chuyên khoa và `top_k`.
- `POST /analyze`: chuyển ca thành truy vấn, tìm nguồn phù hợp và gọi `generate_report()`. Với chuyên khoa tự động, endpoint tìm sơ bộ trên toàn kho rồi dùng chuyên khoa của kết quả đầu tiên. Nếu không có nguồn, endpoint trả nhận định an toàn cùng thông báo thiếu nguồn.
- `POST /feedback`: ghi ghi chú bác sĩ và thời điểm vào `data/clinician_feedback.jsonl`.

Các lỗi dịch vụ lập chỉ mục, tìm kiếm và phân tích được chuyển thành HTTP 503. `schemas.py` xác thực request; các module trong `services` thực hiện nghiệp vụ.
