# SIC Clinical RAG

Ứng dụng hỗ trợ bác sĩ tra cứu hướng dẫn và xem xét chẩn đoán sơ bộ. Backend dùng FastAPI; giao diện dùng Streamlit; tìm kiếm dùng multilingual-e5 và ChromaDB; phần tạo báo cáo kết nối Gemini.

## Bắt đầu nhanh

1. Cài Python 3.11 trở lên.
2. Sao chép `.env.example` thành `.env`, thêm `GOOGLE_API_KEY` từ Google AI Studio.
3. Chạy `.\run.ps1` trong PowerShell. Script cài thư viện, khởi chạy API nền và mở giao diện Streamlit.
4. API: `http://127.0.0.1:8000`; giao diện: `http://127.0.0.1:8501`; tài liệu API: `http://127.0.0.1:8000/docs`.

Lần đầu chạy, máy cần tải mô hình embedding. Để chạy riêng từng dịch vụ, xem [hướng dẫn cài đặt](docs/setup.md).

## Cấu trúc dự án

- `backend/`: API, schemas, cấu hình và dịch vụ RAG/Gemini.
- `frontend/`: giao diện Streamlit.
- `data/markdown/`: kho tài liệu theo chuyên khoa.
- `evaluation/`: công cụ đánh giá truy xuất và huấn luyện embedding.
- `docs/`: tài liệu kiến trúc, API, dữ liệu, chạy ứng dụng và đánh giá.

Đọc thêm: [kiến trúc](docs/architecture.md) · [API](docs/api.md) · [quản lý kho tri thức](docs/knowledge-base.md) · [đánh giá](docs/evaluation.md) · [cài đặt](docs/setup.md).

Muốn biết từng module Python làm gì, xem [hướng dẫn đọc mã nguồn](docs/code/README.md).

## Phạm vi và lưu ý

Kho hiện có 98 tệp Markdown: 43 Nội tiết, 30 Hô hấp và 25 Tim mạch. PDF dự án ghi tài liệu Tim mạch đang chờ, trong khi workspace có thư mục tài liệu Tim mạch; cần xác minh nguồn và nhờ bác sĩ rà soát trước khi dùng.

Chỉ sử dụng cho bác sĩ và dữ liệu giả định hoặc đã ẩn danh. Kết quả chỉ hỗ trợ xem xét, không thay bác sĩ quyết định hay kê đơn. Không nhập dữ liệu nhận dạng người bệnh. Ghi chú hiệu chỉnh được lưu cục bộ tại `data/clinician_feedback.jsonl`.
