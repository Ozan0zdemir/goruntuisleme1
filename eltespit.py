import cv2
import mediapipe as mp

# MediaPipe Hands çözümünü başlat
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# MediaPipe çizim araçlarını başlat
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    
    # Görüntüyü MediaPipe'a uygun hale getir (BGR'dan RGB'ye)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # El tespiti işlemini gerçekleştir
    results = hands.process(frame_rgb)

    # Parmak sayısını tutacak değişken
    finger_count = 0
    
    # Eğer sonuçlar varsa (yani el tespit edildiyse)
    if results.multi_hand_landmarks:
        # Hangi elin ne olduğunu belirlemek için
        if results.multi_handedness:
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Tespit edilen elin sol mu yoksa sağ mı olduğunu al
                handedness = results.multi_handedness[i].classification[0].label
                
                # Başparmak kontrolü
                if handedness == 'Right': # Sağ el için
                    # Başparmak ucu, bir sonraki eklemden daha soldaysa parmak açık
                    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
                        finger_count += 1
                elif handedness == 'Left': # Sol el için
                    # Başparmak ucu, bir sonraki eklemden daha sağdaysa parmak açık
                    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
                        finger_count += 1
                
                # Diğer parmakların kontrolü
                # Bu kısım her iki el için de aynı mantıkta çalışır (dikey kontrol)
                if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y:
                    finger_count += 1
                if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y:
                    finger_count += 1
                if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y:
                    finger_count += 1
                if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y:
                    finger_count += 1
                
                # Tespit edilen elin iskeletini çiz
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
    # Ekrana parmak sayısını yazdır
    cv2.putText(frame, f'Parmak: {finger_count}', (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
    cv2.imshow('El Tespiti', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()