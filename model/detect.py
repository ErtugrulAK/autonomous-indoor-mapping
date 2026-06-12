import cv2
from ultralytics import YOLO

def start_detection():
    # 1. Modeli Yükle
    try:
        model = YOLO('best.pt') 
        print("Eğitilmiş model (best.pt) başarıyla yüklendi.")
    except Exception:
        print("UYARI: 'best.pt' henüz bulunamadı. Varsayılan 'yolov8n.pt' yükleniyor...")
        model = YOLO('yolov8n.pt')

    # 2. Bilgisayarın Kendi Kamerası (0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("HATA: Bilgisayar kamerası açılamadı.")
        return

    print("Yerel kamera başlatıldı. Çıkmak için 'q' tuşuna basın.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Tespit yap
        results = model(frame, conf=0.5)

        # Sonuçları çiz
        annotated_frame = results[0].plot()

        # Pencerede göster
        cv2.imshow("Robot Gozu - Yerel Kamera", annotated_frame)

        # 'q' tuşuna basılırsa çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_detection()


