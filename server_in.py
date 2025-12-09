from flask import Flask, jsonify
from License_Plate import plate_ocr
from Face_Recognition import face_module
from Data_Processing.basic_processing import *
from firebase_admin import firestore
import time
import os
import uuid
import threading

unique_id = 0
current_status = "IDLE"
# Initialize Firebase Storage
bucket = init_firebase_storage()
db = init_firebase_db()
doc_ref = db.collection("stats").document("car_count")

# Folder save image download from firebase storage
LOCAL_DIR = "downloads"
os.makedirs(LOCAL_DIR, exist_ok=True)

PORT = 5000
app = Flask(__name__)

def get_all_images(download_dir="./downloads"):
    # Các định dạng ảnh cần lấy
    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp")

    # Kiểm tra thư mục tồn tại
    if not os.path.exists(download_dir):
        raise FileNotFoundError(f"Thư mục '{download_dir}' không tồn tại")

    # Lấy danh sách tất cả file ảnh
    return [
        os.path.join(download_dir, f)
        for f in os.listdir(download_dir)
        if f.lower().endswith(image_extensions)
    ]

# #download all images
# def download_all_images():
#     images = []
#     blobs = bucket.list_blobs(prefix='data/')
#     for blob in blobs:
#         file_name = blob.name.split('/')[-1]
#         if not file_name:
#             continue
#         local_path = os.path.join(LOCAL_DIR, file_name)
#         blob.download_to_filename(local_path)
#         print(f"[FIREBASE] Đã tải: {file_name}")
#         images.append((local_path, blob))
#     return images

def download_all_images():
    images = []
    blobs = bucket.list_blobs(prefix='data/')

    for blob in blobs:
        # Bỏ split(), giữ nguyên blob.name
        file_name = blob.name.replace("data/", "")  

        if file_name == "":
            continue

        local_path = os.path.join(LOCAL_DIR, file_name)

        blob.download_to_filename(local_path)
        print(f"[FIREBASE] Đã tải: {blob.name}")

        # Lưu EXACT blob (không đổi tên)
        images.append((local_path, blob))

    return images


def get_face_plate(images_paths) :
    f_img = face_embedding = None
    p_img = p_path = p_ocr = None  
    for img_path in images_paths:
        full_img, face_img, embedding = face_module.extract_face_and_embedding(img_path)
        if face_img is not None:
            f_img = full_img 
            face_embedding = embedding
            break
    for img_path in images_paths:
        p_path, scores = plate_ocr.crop_license_plate_for_recognize(img_path)
        if p_path is not None : 
            p_ocr, p_img = plate_ocr.recognize_plate(p_path)
            break
    if p_ocr is None or face_embedding is None :
        return None, None, None, None
    return f_img, face_embedding, p_img, p_ocr


#Processing all images
def process_all_images(images):
    #images = download_all_images()
    if not images:
        return None, None, None, None
    
    local_paths = [local_path for local_path, _ in images]
    #local_paths = [local_path for local_path in images]
    f_img, face_embedding, p_img, p_ocr = get_face_plate(local_paths)
    # Xóa ảnh sau khi xử lý
    for local_path, blob in images:
        try:
            blob.delete()  # Xóa file trên Firebase
            print(f"Đã xóa trên Firebase: {blob.name}")
        except Exception as e:
            print(f"Lỗi xóa {blob.name}: {e}")
    if f_img is None or face_embedding is None or p_img is None or p_ocr is None:
        return None, None, None, None
    return f_img, face_embedding, p_img, p_ocr
            


def programing() :
    global current_status, unique_id
    current_status = "PROCESSING"
    print(" Xử lý ảnh từ Firebase")
    img = download_all_images()
    face_img, face_embedding, p_img, p_ocr = process_all_images(img)
    if face_img is None :
        current_status = "FAIL_IN"
        print("Lưu thông tin thất bại")
        return "FAIL_IN"
    unique_id = uuid.uuid4()
    face_url = upload_image(bucket, face_img, unique_id, "face_in")

    # Upload ảnh plate bình thường
    plate_url = upload_image(bucket, p_img, unique_id, "plate_in")
    write_log_in(
    db=db,
    face_embedding=face_embedding,
    plate=p_ocr,
    image_face=face_url,
    image_lp=plate_url
    )
    current_status = "PASS"
    print("Lưu thông tin thành công")
    return "PASS"


@app.route("/trigger-process", methods=["GET"])
def trigger_process():
    global current_status
    
    if current_status == "PROCESSING":
        print("Đang xử lý")
        return "BUSY", 200 
        
    print("Bắt đầu chạy chương trình")
    current_status = "PROCESSING"
    
    thread = threading.Thread(target=programing)
    thread.start()
    
    
    return "STARTED", 200

@app.route("/check-status", methods=["GET"])
def check_status():
    global current_status
    return current_status, 200

@app.route("/", methods=["GET"])
def index():
    return "AIoT Server (Polling Mode) is running!", 200

 
if __name__ == "__main__":
    print(f"🚀 Server đang chạy trên 0.0.0.0:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=True)

    




