from ultralytics import YOLO

def on_train_epoch_end(trainer):
    epoch = trainer.epoch + 1
    epochs = trainer.epochs
    percent = (epoch / epochs) * 100
    print(f"\n[BİLGİ] Eğitim İlerlemesi: %{percent:.2f} (Epoch {epoch}/{epochs})\n")

def train_model():
    # En hafif model olan 'yolov8n.pt' (nano) ile başlıyoruz. 
    # Robotlar için en hızlısı budur.
    model = YOLO('yolov8n.pt') 

    # İlerleme yüzdesini göstermek için callback ekle
    model.add_callback("on_train_epoch_end", on_train_epoch_end)

    # Eğitimi başlat
    # data: Veri seti yapılandırma dosyası (data.yaml)
    # epochs: Veri setinin kaç kez taranacağı (Başlangıç için 50-100 önerilir)
    # imgsz: Görüntü boyutu (Genelde 640)
    results = model.train(
        data='master_data.yaml', 
        epochs=50, 
        imgsz=640, 
        device='0' # GPU (RTX 2060) kullanımı için '0' olarak ayarlandı
    )
    
    print("Eğitim tamamlandı. En iyi model 'runs/detect/train/weights/best.pt' konumuna kaydedildi.")

if __name__ == "__main__":
    train_model()
