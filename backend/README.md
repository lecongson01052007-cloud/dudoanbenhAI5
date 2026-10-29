# Backend

Backend được chia theo trách nhiệm:

- `main.py`: khởi tạo FastAPI.
- `routes.py`: nhận request và gọi dịch vụ.
- `schemas.py`: xác thực dữ liệu đầu vào.
- `config.py`: nạp `.env`, khai báo đường dẫn/mô hình.
- `services/knowledge_base.py`: nạp Markdown, embeddings, ChromaDB và tìm kiếm.
- `services/gemini.py`: tạo prompt, gọi LLM và lọc trích dẫn.

Chạy từ thư mục gốc dự án: `.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload`.
