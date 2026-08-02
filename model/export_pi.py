from ultralytics import YOLO
import os

def export_for_pi():
    """
    Exports a trained PyTorch weights file ('best.pt') to NCNN model format,
    optimized for lightweight edge deployment on Raspberry Pi systems.
    """
    model_file = 'best.pt'
    
    if not os.path.exists(model_file):
        print(f"ERROR: Weights file '{model_file}' was not found. Please place 'best.pt' in this directory.")
        return

    print(f"--- Exporting '{model_file}' to NCNN format... ---")
    
    try:
        model = YOLO(model_file)
        
        # Export to NCNN format
        # imgsz=320: Optimal speed/accuracy trade-off for Raspberry Pi 3 hardware
        # half=True: FP16 precision acceleration
        export_path = model.export(format='ncnn', imgsz=320, half=True)
        
        print("\n" + "=" * 40)
        print("MODEL EXPORT SUCCESSFUL!")
        print(f"NCNN model export folder: {export_path}")
        print("Transfer this directory along with 'detect_pi.py' to your Raspberry Pi.")
        print("=" * 40)
        
    except Exception as e:
        print(f"An error occurred during model export: {e}")

if __name__ == "__main__":
    export_for_pi()
