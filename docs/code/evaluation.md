# Giải thích script đánh giá và huấn luyện

## `evaluation/retrieval_eval.py`

Đo Hit@5 trên JSONL đã được nhóm duyệt:

1. `read_docs()` đọc các file Markdown và chia nội dung theo tiêu đề.
2. `main()` nạp ca từ `--cases`, nạp mô hình `--model`, tạo vector cho đoạn tài liệu.
3. Với từng câu hỏi, tính tương đồng cosine với kho, lấy 5 đoạn đầu và kiểm tra khớp `relevant_source`/`relevant_section`.
4. In tổng số ca, số hit và tỷ lệ `hit_at_5` dạng JSON.

Lệnh mẫu:

```powershell
.\.venv\Scripts\python.exe evaluation/retrieval_eval.py --cases evaluation/test.jsonl --model intfloat/multilingual-e5-base
```

## `evaluation/train_e5.py`

Fine-tune mô hình embedding từ cặp query/positive passage đã được xác minh:

- Đọc JSONL từ `--train`; mỗi dòng cần `query` và `positive_text`.
- Tạo `InputExample`, dùng `MultipleNegativesRankingLoss` và huấn luyện qua `SentenceTransformer.fit()`.
- Ghi mô hình ra thư mục `--output`.

Lệnh mẫu:

```powershell
.\.venv\Scripts\python.exe evaluation/train_e5.py --train evaluation/train.jsonl --output models/e5-clinical
```

Không đưa ca test vào train. Đánh giá mô hình gốc và mô hình fine-tune trên cùng tập test để so sánh. Xem [hướng dẫn định dạng dữ liệu](../evaluation/README.md).
