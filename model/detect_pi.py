import cv2
from ultralytics import YOLO
import time
import os

def start_pi_detection():
    # 1. Model Seçimi
    # Pi 3 için NCNN formatı en hızlısıdır. 
    # Eğer henüz 'best_ncnn_model' klasörün yoksa önce export etmelisin.
    model_path = 'best_ncnn_model' 
    
    if not os.path.exists(model_path):
        print(f"UYARI: {model_path} bulunamadı! Standart modelden devam ediliyor...")
        print("İPUCU: Daha fazla hız için modelini NCNN formatına çevirmelisin.")
        model_path = 'best.pt'

    try:
        # task='detect' parametresi Pi'de yüklemeyi hızlandırabilir
        model = YOLO(model_path, task='detect')
        print(f"Model yüklendi: {model_path}")
    except Exception as e:
        print(f"HATA: Model yüklenemedi: {e}")
        return

    # 2. Kamera Ayarları (Telefon Kamerası - IP Webcam)
    # Telefonundaki IP Webcam uygulamasında yazan adresi buraya gir:
    url = 'http://192.168.1.100:8080/video' 
    cap = cv2.VideoCapture(url)
    
    # Çözünürlük ayarı IP kamerada ağ hızına göre otomatikleşir
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("HATA: Kamera açılamadı.")
        return

    print("--- Raspberry Pi Optimizasyonu Aktif ---")
    print("Çıkmak için 'q' tuşuna basın.")

    # Pencere boyutunu ayarla (Dikey görüntü için 480x640)
    cv2.namedWindow("Pi3 Robot Vision", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Pi3 Robot Vision", 480, 640)

    prev_time = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Görüntüyü 90 derece sağa döndür (Telefon dik tutuluyorsa)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        # 3. Tespit Yap (Önemli Parametreler)
        # imgsz: 160, 192, 224, 320 gibi düşük değerler hızı artırır.
        # conf: Güven eşiği
        # half: True (Eğer NCNN kullanıyorsan FPS artırabilir)
        # stream: True (Bellek kullanımı için daha iyidir)
        results = model.predict(
            source=frame, 
            imgsz=320, 
            conf=0.4, 
            verbose=False, 
            stream=True
        )

        for r in results:
            # Sonuçları çiz
            annotated_frame = r.plot()
            
            # FPS Hesapla
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time
            
            # Ekrana FPS ve Bilgi Yaz
            cv2.putText(annotated_frame, f"Pi3 FPS: {fps:.1f}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # 4. Görüntüleme (Opsiyonel)
            # Eğer robotu sadece terminalden izleyeceksen imshow'u yorum satırına alabilirsin.
            cv2.imshow("Pi3 Robot Vision", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_pi_detection()
