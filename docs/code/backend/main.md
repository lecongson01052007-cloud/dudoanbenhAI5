# `backend/main.py`

## Vai trò

Tạo ứng dụng FastAPI và kết nối các endpoint đã khai báo trong `routes.py`.

## Thành phần chính

- Tạo đối tượng `app` với tên, phiên bản và mô tả API.
- Thêm `CORSMiddleware`; cấu hình hiện cho phép mọi origin, method và header.
- Gắn `router` vào ứng dụng bằng `app.include_router(router)`.

Khi chạy `uvicorn backend.main:app`, Uvicorn nạp module này và phục vụ đối tượng `app`. Xử lý endpoint nằm trong `routes.py`, nghiệp vụ được chuyển tiếp tới các module `services`.
