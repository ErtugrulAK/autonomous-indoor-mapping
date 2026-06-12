import cv2
from ultralytics import YOLO
import time

def start_phone_detection():
    # 1. Modeli Yükle
    # NOT: Eğitim bitince Colab'dan aldığın 'best.pt' dosyasını bu klasöre koymalısın.
    try:
        model = YOLO('best.pt') 
        print("Eğitilmiş model (best.pt) başarıyla yüklendi.")
    except Exception:
        print("UYARI: 'best.pt' henüz bulunamadı. Varsayılan 'yolov8n.pt' yükleniyor...")
        model = YOLO('yolov8n.pt')

    # 2. Telefonun IP Kamera Adresi (IP Webcam uygulamasındaki adres)
    url = 'http://192.168.1.100:8080/video'

    # 3. Kamerayı Başlat
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        print("HATA: Kamera akışına bağlanılamadı. Wi-Fi ve IP adresini kontrol edin.")
        return

    print(f"Telefon kamerasına bağlandı: {url}")
    print("Çıkmak için 'q' tuşuna basın.")

    # Pencere boyutunu ayarla (Dikey görüntü için 480x640)
    cv2.namedWindow("Robot Vision - Telefon Kamerasi", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Robot Vision - Telefon Kamerasi", 480, 640)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kare alınamadı, yayın kesilmiş olabilir.")
            break

        # Görüntüyü 90 derece sağa döndür
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        # Tespit yap
        start_time = time.time()
        results = model(frame, conf=0.5, verbose=False)
        end_time = time.time()

        # FPS hesapla
        fps = 1 / (end_time - start_time)

        # Sonuçları çiz
        annotated_frame = results[0].plot()
        
        # Ekrana FPS yaz
        cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Pencerede göster
        cv2.imshow("Robot Vision - Telefon Kamerasi", annotated_frame)

        # 'q' tuşuna basılırsa çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_phone_detection()
