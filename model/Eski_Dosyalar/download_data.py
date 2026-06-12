import os
from roboflow import Roboflow

# NOT: Roboflow'dan kendi API anahtarınızı almanız gerekmektedir.
# https://app.roboflow.com/settings/api adresinden alabilirsiniz.

def download_dataset():
    # Sizin API anahtarınız eklendi
    rf = Roboflow(api_key="BOUeK4YXd3nc5hMykduY") 
    
    # Örnek: Kapı ve Pencere veri setini indir
    project = rf.workspace("project-u09sc").project("window-and-door-detection")
    dataset = project.version(1).download("yolov8")
    
    print(f"Veri seti başarıyla indirildi: {dataset.location}")

if __name__ == "__main__":
    print("Veri indirme işlemi başlatılıyor...")
    download_dataset() 
