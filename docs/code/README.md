# Hướng dẫn đọc mã nguồn

Các trang dưới đây giải thích từng file code trong dự án, đường đi của dữ liệu và nơi cần sửa khi muốn đổi chức năng.

- [Backend](backend.md): các file Python trong `backend/`.
- [Giao diện](frontend.md): Streamlit trong `frontend/streamlit_app.py`.
- [Đánh giá và huấn luyện](evaluation.md): hai script Python trong `evaluation/`.
- [Cấu hình và khởi chạy](project-files.md): `run.ps1`, `requirements.txt`, `.env.example`.

## Luồng chính

```text
Streamlit form
    → FastAPI route
    → schema validation
    → multilingual-e5 query embedding
    → ChromaDB top-k retrieval
    → Gemini report with retrieved citations
    → Streamlit result and source excerpts
```

Tra cứu kho chỉ dùng các bước embedding và ChromaDB. Phân tích ca bệnh gọi thêm Gemini để sinh báo cáo. Xem [kiến trúc tổng thể](../architecture.md) để biết thêm về dữ liệu và thư mục runtime.
