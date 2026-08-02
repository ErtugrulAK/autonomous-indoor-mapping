from ultralytics import YOLO

def on_train_epoch_end(trainer):
    epoch = trainer.epoch + 1
    epochs = trainer.epochs
    percent = (epoch / epochs) * 100
    print(f"\n[INFO] Training Progress: {percent:.2f}% (Epoch {epoch}/{epochs})\n")

def train_model():
    # Initialize with lightweight pre-trained model ('yolov8n.pt')
    model = YOLO('yolov8n.pt') 

    # Register progress tracking callback
    model.add_callback("on_train_epoch_end", on_train_epoch_end)

    # Initiate model training
    # data: Dataset configuration YAML path
    # epochs: Number of complete dataset passes (Recommended: 50-100)
    # imgsz: Image resolution (Default: 640)
    # device: GPU device index ('0' for CUDA GPU, 'cpu' for CPU training)
    results = model.train(
        data='master_data.yaml', 
        epochs=50, 
        imgsz=640, 
        device='0'
    )
    
    print("Training complete. Best model weights saved to 'runs/detect/train/weights/best.pt'.")

if __name__ == "__main__":
    train_model()
