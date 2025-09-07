import cv2
from deepface import DeepFace
import time
import threading

# Kamerayı başlat
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera açılamadı. Lütfen bağlantıyı kontrol edin.")
    exit()

# FPS hesaplama için zaman
prev_time = 0

# Duygu sonucu
dominant_emotion = "Bilinmiyor"

# Analizi arka planda çalıştıracak fonksiyon
def analyze_frame(frame):
    global dominant_emotion
    try:
        result = DeepFace.analyze(
            frame,
            actions=['emotion'],
            enforce_detection=False,
            silent=True,
            detector_backend="retinaface"  # daha dengeli
        )
        dominant_emotion = result[0]['dominant_emotion']
    except:
        dominant_emotion = "Yüz algılanamadı"

# Thread kontrolü
analysis_thread = None
frame_count = 0
analyze_interval = 10  # her 10 karede bir analiz başlat

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kare alınamadı. Çıkılıyor...")
        break

    frame_count += 1

    # Thread boşsa ve analiz zamanı geldiyse başlat
    if frame_count % analyze_interval == 0:
        if analysis_thread is None or not analysis_thread.is_alive():
            analysis_thread = threading.Thread(target=analyze_frame, args=(frame.copy(),))
            analysis_thread.start()

    # Çerçeveye duyguyu yaz
    cv2.putText(frame, f"Duygu: {dominant_emotion}", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # FPS hesaplama
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
    prev_time = curr_time

    cv2.putText(frame, f"FPS: {fps:.2f}", (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.imshow("Duygu Analizi", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
