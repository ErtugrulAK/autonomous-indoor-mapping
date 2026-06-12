from ultralytics import YOLO
import os

def export_for_pi():
    """
    Bu script, bilgisayarında eğittiğin 'best.pt' modelini 
    Raspberry Pi 3'te en hızlı çalışacak format olan NCNN'e çevirir.
    """
    model_file = 'best.pt'
    
    if not os.path.exists(model_file):
        print(f"HATA: {model_file} bulunamadı. Lütfen önce modelini bu klasöre kopyala.")
        return

    print(f"--- {model_file} NCNN formatına dönüştürülüyor... ---")
    
    try:
        model = YOLO(model_file)
        
        # NCNN formatına dışa aktar
        # imgsz=320: Pi 3 için ideal hız/doğruluk dengesi
        # half=True: FP16 hassasiyeti ile daha hızlı çalışma
        export_path = model.export(format='ncnn', imgsz=320, half=True)
        
        print("\n" + "="*30)
        print("BAŞARILI!")
        print(f"Pi 3'e kopyalaman gereken klasör: {export_path}")
        print("Bu klasörü ve 'detect_pi.py' dosyasını Raspberry Pi'ye taşıyabilirsin.")
        print("="*30)
        
    except Exception as e:
        print(f"Dönüştürme sırasında hata oluştu: {e}")

if __name__ == "__main__":
    export_for_pi()
