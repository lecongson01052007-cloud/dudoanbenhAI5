# Kiến trúc ứng dụng

## Luồng xử lý

1. Streamlit thu thập thông tin ca bệnh qua form hoặc câu hỏi tra cứu.
2. Giao diện gửi JSON tới FastAPI.
3. Dịch vụ kho tri thức chia Markdown theo tiêu đề, gắn chuyên khoa/tên bệnh/nguồn, mã hóa bằng multilingual-e5 và lưu vector trong ChromaDB.
4. Truy vấn được mã hóa theo tiền tố `query:`; các đoạn tài liệu dùng tiền tố `passage:`. Chroma trả về các đoạn gần nhất.
5. Với phân tích ca, Gemini nhận ca bệnh cùng các đoạn đã truy xuất và tạo báo cáo JSON có trích dẫn. API lọc mã trích dẫn để chỉ giữ các nguồn đã cung cấp cho mô hình.

## Các phần mã nguồn

- `backend/main.py`: tạo FastAPI app và cấu hình middleware.
- `backend/routes.py`: endpoint health, danh mục, ingest, search, analyze, feedback.
- `backend/schemas.py`: kiểu dữ liệu đầu vào và kiểm tra giới hạn trường.
- `backend/config.py`: đường dẫn dự án, cấu hình môi trường và tên chuyên khoa.
- `backend/services/knowledge_base.py`: đọc Markdown, chia đoạn, embeddings, ChromaDB, tìm kiếm.
- `backend/services/gemini.py`: prompt lâm sàng, gọi Gemini và kiểm tra trích dẫn.
- `frontend/streamlit_app.py`: ba trang giao diện bác sĩ.

## Thư mục dữ liệu sinh ra

- `vector_db/`: chỉ mục ChromaDB bền vững; có thể tạo lại từ Markdown.
- `.venv/`: môi trường Python cục bộ.
- `data/clinician_feedback.jsonl`: ghi chú bác sĩ, không chứa payload ca bệnh.

Các thư mục sinh ra này được bỏ qua trong Git.
