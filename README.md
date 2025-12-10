# Hệ thống quản lý bãi xe thông minh cho phép gửi và lấy xe
* Khi vào gửi xe sẽ lấy ảnh khuôn mặt và biển số để lưu thông tin.
* Khi xe đi ra lấy cơ sở dữ liệu để kiểm tra có đúng thông tin người gửi.
# Yêu cầu cài đặt
* Cài đặt trên môi trường python 3.11
* Cài đặt yolov5.
* Cài đặt các thư viện trong requirements.txt.
* Tải file trọng số yolov5su.pt : https://www.bing.com/search?qs=SC&pq=yolov5su.pt+d&sk=CSYN1&sc=3-13&q=yolov5s.pt+download&cvid=59aab2c1fe9c49c1a213f540989ba30f&gs_lcrp=EgRlZGdlKgYIARAAGEAyBggAEEUYOTIGCAEQABhAMgYIAhAAGEAyCAgDEOkHGPxV0gEIMTMyNWowajSoAgiwAgE&FORM=ANAB01&PC=LCTS
* Tải các file trọng số :
  - Phát hiện biển số : [https://drive.google.com/drive/u/0/folders/18UhhcOFV1Ew-98G3BAfpE8v2D9B-qmJh](https://drive.google.com/drive/u/0/folders/18UhhcOFV1Ew-98G3BAfpE8v2D9B-qmJh)
  - OCR biển số : [https://drive.google.com/drive/u/0/folders/11hXqQFjcrLv5xR5ePFQD8uAIo9oBaplR](https://drive.google.com/drive/u/0/folders/11hXqQFjcrLv5xR5ePFQD8uAIo9oBaplR)
  - Sau khi tải về local đọc file License_Plate/plate_ocr.py để truyền trọng số.
* Tạo các database và storage trên firebase và lấy các file .json của database và storage.
* Đọc comment trong file Data_Processing/basic_processing.py để biết cách truyền đường dẫn file .json.
* Chạy lệnh python server_in.py để kiểm tra luồng đi vào của xe và python server_out trong terminal để kiểm tra luồng xác thực.
* ```php

echo ("highlight code");

```
