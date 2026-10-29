# Kho tri thức và tài liệu nguồn

## Cấu trúc

Đặt Markdown trong `data/markdown/`, chia thư mục theo chuyên khoa. Hệ thống dùng thư mục làm nhãn chuyên khoa chính; metadata có thể ghi tiểu chuyên khoa.

Các tiêu đề Markdown `#`, `##`, `###` là ranh giới chia đoạn. Mỗi đoạn giữ các trường: `specialty`, `disease`, `section`, `source`, `review_status`. Phần dài được chia cửa sổ để truy xuất.

## Metadata gợi ý

```yaml
---
title: Tên bệnh
specialty: Hô hấp
source: Tên hướng dẫn hoặc tài liệu gốc
review_status: needs_clinical_review
---
```

Nên ghi rõ tài liệu gốc, năm ban hành và trang nếu có. Trạng thái metadata không chứng minh tài liệu đã được bác sĩ duyệt.

## Nạp lại

Từ trang Quản lý tài liệu tải `.md` hoặc gửi `POST /ingest`. Chỉ mục cũ được thay bằng chỉ mục mới để tránh trùng lặp. PDF cần chuyển đổi sang Markdown và kiểm tra nội dung/trích dẫn trước khi nạp.

Kho hiện có 43 tài liệu Nội tiết, 30 Hô hấp, 25 Tim mạch. Số lượng đoạn có thể thay đổi khi nội dung được chỉnh sửa.
