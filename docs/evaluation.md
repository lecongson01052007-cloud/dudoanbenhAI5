# Đánh giá truy xuất và huấn luyện embedding

Chưa có bộ ca đánh giá đã được bác sĩ duyệt trong dự án; không nên báo cáo số liệu giả. Hướng dẫn lệnh và định dạng JSONL chi tiết ở [evaluation/README.md](../evaluation/README.md).

## Quy trình đề xuất

1. Tạo truy vấn lâm sàng giả định/ẩn danh và đoạn tài liệu liên quan đã được xác minh.
2. Chia train/test theo bệnh để hạn chế rò rỉ giữa hai tập.
3. Chạy `evaluation/retrieval_eval.py` trên tập test để lấy Hit@5 của embedding gốc.
4. Fine-tune chỉ với tập train bằng `evaluation/train_e5.py`.
5. Chạy lại đúng tập test và so sánh Hit@5 trước/sau.
6. Đánh giá riêng chất lượng gợi ý chẩn đoán, trích dẫn và các ca thiếu thông tin; nhờ bác sĩ rà soát mẫu.

Không đưa ca test vào tài liệu, prompt hoặc dữ liệu huấn luyện. Báo cáo rõ số ca, cách tạo nhãn và người duyệt.
