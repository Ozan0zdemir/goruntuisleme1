import cv2
import mediapipe as mp
import time

# --- Mediapipe Modüllerini ve Parametrelerini Başlatma ---
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Yüz ağı modeli oluşturma
# Model daha az yüz algılama (1 yüz) ve düşük güven seviyesiyle (0.5) optimize edilmiştir.
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.5,  # Varsayılan değere yükseltildi
    min_tracking_confidence=0.5)  # Varsayılan değere yükseltildi

# --- Sabit Değerler ve Yardımcı Fonksiyonlar ---
# Göz noktaları için sabit listeler
LEFT_EYE_POINTS = [33, 133, 159, 144, 153, 158]
RIGHT_EYE_POINTS = [362, 263, 386, 373, 380, 382]

def get_eye_center(landmarks, points, width, height):
    """
    Belirtilen göz noktalarının ortalama koordinatlarını hesaplar.
    """
    x_coords = [landmarks.landmark[p].x for p in points]
    y_coords = [landmarks.landmark[p].y for p in points]
    x_center = int(sum(x_coords) / len(x_coords) * width)
    y_center = int(sum(y_coords) / len(y_coords) * height)
    return x_center, y_center

# --- Ana İşlem Döngüsü ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Hata: Kamera açılamadı.")
    exit()

prev_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # FPS hesaplama
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # Görüntü işleme
    frame = cv2.flip(frame, 1)  # Yatayda ters çevirme
    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Yüz algılama
    results = face_mesh.process(frame_rgb)

    # Görüntü üzerine çizim yapma
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Yüz ağını çizmek için Mediapipe'ın varsayılan çizim özelliklerini kullanma
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=mp_drawing.DrawingSpec(thickness=1, circle_radius=1),
                connection_drawing_spec=mp_drawing.DrawingSpec(thickness=1, circle_radius=1))

            # Göz merkezlerini bul ve çiz
            lx, ly = get_eye_center(face_landmarks, LEFT_EYE_POINTS, w, h)
            rx, ry = get_eye_center(face_landmarks, RIGHT_EYE_POINTS, w, h)

            cv2.circle(frame, (lx, ly), 5, (0, 0, 255), -1)  # Sol göz
            cv2.circle(frame, (rx, ry), 5, (0, 0, 255), -1)  # Sağ göz

    else:
        # Yüz bulunamadı mesajını gösterme
        cv2.putText(frame, "Yuz bulunamadi!", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # FPS bilgisini ekrana yazma
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.imshow('Canli Yuz ve Goz Tespiti (Gelistirilmis)', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- Kaynakları Serbest Bırakma ---
cap.release()
cv2.destroyAllWindows()