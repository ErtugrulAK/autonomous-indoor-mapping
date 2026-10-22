import cv2
from ultralytics import YOLO
import time
import os

def start_pi_detection():
    # 1. Model Format Selection
    # NCNN format delivers optimal inference speeds on Raspberry Pi devices.
    model_path = os.environ.get('NCNN_MODEL_PATH', 'best_ncnn_model')
    
    if not os.path.exists(model_path):
        print(f"WARNING: '{model_path}' not found! Falling back to PyTorch model...")
        print("HINT: Convert your model to NCNN format using 'export_pi.py' for optimal performance.")
        model_path = 'best.pt'

    try:
        model = YOLO(model_path, task='detect')
        print(f"Model successfully loaded: {model_path}")
    except Exception as e:
        print(f"ERROR: Model initialization failed: {e}")
        return

    # 2. Camera Configuration (IP Webcam Endpoint; override with CAMERA_SOURCE)
    url = os.environ.get('CAMERA_SOURCE', 'http://192.168.1.100:8080/video')
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        print("ERROR: Could not open camera stream.")
        return

    print("--- Raspberry Pi Optimized Vision Running ---")
    print("Press 'q' to quit.")

    # Configure rendering window dimensions
    cv2.namedWindow("Pi3 Robot Vision", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Pi3 Robot Vision", 480, 640)

    prev_time = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Rotate frame for vertical camera orientation
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        # 3. Model Inference (Optimized Execution Parameters)
        # Reduced imgsz (e.g. 320) speeds up processing on low-power edge hardware.
        results = model.predict(
            source=frame, 
            imgsz=320, 
            conf=0.4, 
            verbose=False, 
            stream=True
        )

        for r in results:
            annotated_frame = r.plot()
            
            # Compute FPS metric
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
            prev_time = curr_time
            
            # Render performance metrics on frame
            cv2.putText(annotated_frame, f"Pi3 FPS: {fps:.1f}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Display feed window
            cv2.imshow("Pi3 Robot Vision", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_pi_detection()
