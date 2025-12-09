import face_recognition
import numpy as np
from PIL import Image
import cv2 
from scipy.spatial.distance import cosine
from deepface import DeepFace

# MODEL_NAME = "ArcFace"
# # Dùng RetinaFace để bắt mặt cực chuẩn (kể cả mờ/nghiêng)
# DETECTOR_BACKEND = "retinaface"
# def extract_face_and_embedding(image_path, target_size=(160, 160)):
#     """
#     Hàm thay thế dùng DeepFace (ArcFace + RetinaFace).
#     Input: Đường dẫn ảnh.
#     Output: (image_path, face_pil, embedding)
#     """
#     try:
#         embedding_objs = DeepFace.represent(
#             img_path = image_path,
#             model_name = MODEL_NAME,
#             detector_backend = DETECTOR_BACKEND,
#             align = True,
#             enforce_detection = True
#         )

#         # Lấy kết quả khuôn mặt đầu tiên (trong trường hợp ảnh có nhiều người)
#         result = embedding_objs[0]
#         embedding = result["embedding"]
#         facial_area = result["facial_area"] # {'x': 10, 'y': 20, 'w': 100, 'h': 100}

        
#         img_bgr = cv2.imread(image_path)
#         img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
#         x = facial_area['x']
#         y = facial_area['y']
#         w = facial_area['w']
#         h = facial_area['h']

#         x = max(0, x)
#         y = max(0, y)
#         face_crop = img_rgb[y:y+h, x:x+w]
        
#         # Convert sang PIL và Resize
#         face_pil = Image.fromarray(face_crop)
#         resized_face_pil = face_pil.resize(target_size)

#         # 3. Trả về đúng định dạng cũ của bạn
#         return image_path, resized_face_pil, embedding

#     except ValueError:
#         # Trường hợp DeepFace không tìm thấy mặt
#         print(f"Không tìm thấy khuôn mặt trong: {image_path}")
#         return None, None, None
        
#     except Exception as e:
#         
#         return None, None, None


# 3. Hàm tính cosine similarity giữa 2 vector
# def cosine_similarity(emb1, emb2, threshold=0.95):
#     if emb1 is None or emb2 is None:
#         return False, 0.0
#     # Tính Cosine Distance (Càng NHỎ càng giống)
#     # distance = cosine(emb1, emb2)
    
#     # is_match = distance <= threshold
#     # return is_match, distance
    
#     dist = np.linalg.norm(emb1 - emb2)

#     # So sánh với threshold
#     is_match = dist <= threshold

#     return is_match, dist


def extract_face_and_embedding(image_path, target_size=(160, 160)):
    image = face_recognition.load_image_file(image_path)
    
    face_locations = face_recognition.face_locations(image, model='hog')
    if len(face_locations) == 0:
        return image_path, None, None
    
    top, right, bottom, left = face_locations[0]

    # Crop để hiển thị
    face_crop = image[top:bottom, left:right]
    face_pil = Image.fromarray(face_crop).resize(target_size)

    # Không dùng CLAHE cho embedding
    encodings = face_recognition.face_encodings(
        image,
        known_face_locations=[(top, right, bottom, left)],
        num_jitters=1
    )

    if len(encodings) == 0:
        return image_path, face_pil, None

    return image_path, face_pil, encodings[0]

def cosine_similarity(emb1, emb2, threshold=0.91):
    if emb1 is None or emb2 is None:
        return False

    emb1 = np.array(emb1, dtype=np.float32)
    emb2 = np.array(emb2, dtype=np.float32)

    # Nếu khác shape thì fail
    if emb1.shape != emb2.shape:
        print("Embedding shape mismatch:", emb1.shape, emb2.shape)
        return False, None

    # Tính cosine similarity
    dot = np.dot(emb1, emb2)
    norm = np.linalg.norm(emb1) * np.linalg.norm(emb2)

    if norm == 0:
        return False

    cosine_sim = dot / norm

    # Điều kiện bạn yêu cầu:
    # Nếu cosine < 0.3 thì return False (không khớp)
    if cosine_sim < threshold:
        return False

    # Nếu >= 0.3 thì coi là khớp
    return True








