# Bộ ca kiểm tra và fine-tune e5

Mỗi dòng JSONL trong `train.jsonl` hoặc `test.jsonl` có dạng:

```json
{"query":"Câu hỏi lâm sàng đã được ẩn danh","relevant_source":"noi_tiet_chan-doan/Dai_Thao_Duong_Typ_2_chan-doan.md","relevant_section":"Tiêu chuẩn chẩn đoán","positive_text":"Đoạn hướng dẫn liên quan đã được bác sĩ xác nhận"}
```

`relevant_source` phải khớp tương đối với đường dẫn tệp trong `data/markdown`. Giữ ca kiểm tra riêng, không đưa vào prompt hay tập huấn luyện. Các ca cần được bác sĩ/giảng viên rà soát trước khi dùng và nên chia theo bệnh để tránh rò rỉ giữa train/test.

Đánh giá: `python evaluation/retrieval_eval.py --cases evaluation/test.jsonl --model intfloat/multilingual-e5-base`.

Huấn luyện: `python evaluation/train_e5.py --train evaluation/train.jsonl --output models/e5-clinical`. Sau đó chạy đánh giá lại bằng `--model models/e5-clinical` trên đúng tập test. Cần tự thu thập cặp truy vấn/đoạn tài liệu được xác minh. Không có số liệu nào được điền sẵn trong repo.
