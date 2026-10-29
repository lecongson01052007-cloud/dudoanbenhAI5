# `backend/schemas.py`

## Vai trò

Định nghĩa các mô hình Pydantic mà FastAPI dùng để xác thực và giới hạn dữ liệu request.

## Các mô hình

- `Lab`: tên, giá trị và đơn vị xét nghiệm; có giới hạn độ dài.
- `Case`: tuổi từ 0 đến 120, giới tính theo danh sách cho phép, triệu chứng chính, thời gian, triệu chứng kèm, tiền sử, xét nghiệm và chuyên khoa. Danh sách có giới hạn số phần tử.
- `SearchRequest`: truy vấn 2–3000 ký tự, chuyên khoa và `top_k` từ 1 đến 8.
- `ClinicianFeedback`: ghi chú bắt buộc và chuỗi thời gian.

FastAPI chuyển JSON hợp lệ thành các đối tượng này trước khi gọi endpoint. Dữ liệu sai kiểu hoặc ngoài giới hạn sẽ bị từ chối ở bước xác thực. `Case` cũng được dùng bởi `services/gemini.py`.
