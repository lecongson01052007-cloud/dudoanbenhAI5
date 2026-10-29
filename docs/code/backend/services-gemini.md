# `backend/services/gemini.py`

## Vai trò

Chuyển thông tin ca thành nội dung truy vấn và gọi Gemini để tạo báo cáo JSON dựa trên các nguồn đã truy xuất.

## Hàm chính

### `case_to_query(case)`

Ghép tuổi, giới tính, triệu chứng, thời gian, tiền sử và xét nghiệm thành chuỗi để tìm kiếm trong kho. Trường còn trống được thay bằng thông báo chưa cung cấp hoặc không ghi nhận.

### `generate_report(case, sources)`

1. Kiểm tra `GOOGLE_API_KEY`; nếu thiếu hoặc là giá trị mẫu thì báo lỗi cấu hình.
2. Tạo trích đoạn nguồn kèm mã citation, tên tài liệu và mục.
3. Tạo prompt yêu cầu phản hồi JSON, giới hạn câu trả lời theo ca và nguồn, nêu thông tin thiếu và mức độ khẩn.
4. Gọi Gemini với model cấu hình qua `GEMINI_MODEL` và chế độ JSON.
5. Phân tích JSON; nếu phản hồi sai định dạng thì báo lỗi.
6. Lọc citation để chỉ giữ mã nguồn có trong `sources`.

`routes.py` gọi `case_to_query()` trước khi truy xuất, rồi truyền ca và kết quả vào `generate_report()`. Module này không tự tìm tài liệu.
