import os
from roboflow import Roboflow

# Get your own key at https://app.roboflow.com/settings/api
# and export it as ROBOFLOW_API_KEY before running this script.
ROBOFLOW_API_KEY = os.environ.get("ROBOFLOW_API_KEY")

def download_dataset():
    if not ROBOFLOW_API_KEY:
        raise SystemExit("Set the ROBOFLOW_API_KEY environment variable first.")
    rf = Roboflow(api_key=ROBOFLOW_API_KEY)
    
    # Örnek: Kapı ve Pencere veri setini indir
    project = rf.workspace("project-u09sc").project("window-and-door-detection")
    dataset = project.version(1).download("yolov8")
    
    print(f"Veri seti başarıyla indirildi: {dataset.location}")

if __name__ == "__main__":
    print("Veri indirme işlemi başlatılıyor...")
    download_dataset() 
