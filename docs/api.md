# API

Mọi API JSON chạy tại `http://127.0.0.1:8000`. Có thể xem và gửi yêu cầu thử qua `/docs`.

## `GET /health`

Trả trạng thái backend, danh sách chuyên khoa, trạng thái thư mục dữ liệu và `llm_configured`.

## `GET /documents`

Trả tổng tài liệu/đoạn, số tài liệu mỗi chuyên khoa và danh mục nguồn.

## `POST /search`

```json
{
  "query": "tiêu chuẩn chẩn đoán đái tháo đường type 2",
  "specialty": "Nội tiết",
  "top_k": 5
}
```

`specialty`: `Tất cả`, `Nội tiết`, `Hô hấp`, hoặc `Tim mạch`. `top_k` từ 1 tới 8. Mỗi kết quả có đoạn trích, chuyên khoa, đường dẫn nguồn, điểm tương đồng và mã `S1`, `S2`, …

## `POST /analyze`

```json
{
  "age": 45,
  "sex": "Nam",
  "main_symptom": "khó thở khi gắng sức",
  "duration": "3 ngày",
  "associated_symptoms": ["ho khan"],
  "history": "tăng huyết áp",
  "labs": [{"name": "SpO2", "value": "94", "unit": "%"}],
  "specialty": "Hô hấp"
}
```

`sex`: `Nam`, `Nữ`, `Khác`; `specialty`: `Tự động`, `Nội tiết`, `Hô hấp`, `Tim mạch`. Trả nhận định sơ bộ, chẩn đoán phân biệt, thông tin thiếu, đánh giá có thể cân nhắc, mức khẩn và nguồn.

## `POST /ingest`

Không kèm tệp: lập chỉ mục lại toàn bộ Markdown. Có thể tải một `.md` bằng multipart field `file` (tối đa 5 MB); sau khi lưu, kho được lập chỉ mục lại.

## `POST /feedback`

```json
{"note": "Ghi chú hiệu chỉnh của bác sĩ", "timestamp": "2026-10-29T10:30"}
```

Chỉ lưu ghi chú và thời gian vào JSONL cục bộ, không gửi kèm ca bệnh.
