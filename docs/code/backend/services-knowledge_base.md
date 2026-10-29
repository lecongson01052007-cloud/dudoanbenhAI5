# `backend/services/knowledge_base.py`

## Vai trò

Đọc tài liệu Markdown, chia thành các đoạn, tạo embedding, lưu trong ChromaDB và truy xuất đoạn gần với truy vấn.

## Đọc và chuẩn hóa tài liệu

- `_parse_frontmatter()`: đọc metadata YAML đơn giản ở đầu file.
- `_normalize_specialty()`: suy ra chuyên khoa từ đường dẫn hoặc metadata.
- `_split_document()`: tách nội dung theo heading Markdown, bỏ đoạn quá ngắn, chia đoạn dài và gắn metadata nguồn, mục, bệnh, chuyên khoa, trạng thái rà soát. Có bước thử khôi phục một số file UTF-8 đã bị đọc nhầm qua Windows-1252.
- `read_documents()`: duyệt các file `.md` trong `DATA_DIR`, bỏ qua file không đọc được.
- `document_inventory()`: tổng hợp số file, số đoạn và metadata.

## Embedding và lưu trữ

- `_get_encoder()`: khởi tạo `SentenceTransformer` theo nhu cầu.
- `_get_collection()`: tạo client ChromaDB bền vững tại `VECTOR_DIR` và lấy collection `clinical_guidelines`.
- `ingest_documents()`: có thể xóa index hiện tại, mã hóa theo lô tối đa 64 đoạn với tiền tố `passage:`, rồi upsert vector cùng metadata. ID được tạo từ SHA-1 của nguồn, mục và phần đầu nội dung.
- `ensure_index()`: nạp tài liệu khi collection chưa có dữ liệu.

## Truy xuất

`search_documents(query, specialty, top_k)` mã hóa truy vấn với tiền tố `query:`, lọc theo chuyên khoa trừ khi chọn toàn bộ hoặc tự động, rồi truy vấn Chroma. Kết quả gồm nội dung, metadata, điểm tương đồng và mã citation `S1`, `S2`, ... theo thứ tự trả về.

Thay đổi cách chia đoạn, model embedding hoặc cấu trúc metadata có thể yêu cầu lập chỉ mục lại.
