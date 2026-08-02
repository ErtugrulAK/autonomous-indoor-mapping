import cv2
from ultralytics import YOLO
import time

def start_phone_detection():
    # 1. Load Model Weights
    try:
        model = YOLO('best.pt') 
        print("Custom model ('best.pt') loaded successfully.")
    except Exception:
        print("WARNING: 'best.pt' not found. Falling back to default 'yolov8n.pt'...")
        model = YOLO('yolov8n.pt')

    # 2. IP Webcam Stream Endpoint URL
    url = 'http://192.168.1.100:8080/video'

    # 3. Connect to IP Camera Stream
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        print("ERROR: Failed to connect to IP camera stream. Check Wi-Fi connection and IP URL.")
        return

    print(f"Connected to IP camera stream: {url}")
    print("Press 'q' to quit.")

    # Configure rendering window size (Portrait aspect ratio 480x640)
    cv2.namedWindow("Robot Vision - IP Camera Stream", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Robot Vision - IP Camera Stream", 480, 640)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Stream may have disconnected.")
            break

        # Rotate frame 90 degrees clockwise for portrait smartphone orientation
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        # Measure inference latency
        start_time = time.time()
        results = model(frame, conf=0.5, verbose=False)
        end_time = time.time()

        # Compute Frames Per Second (FPS)
        fps = 1 / (end_time - start_time)

        # Plot detection annotations
        annotated_frame = results[0].plot()
        
        # Render FPS overlay text
        cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display window
        cv2.imshow("Robot Vision - IP Camera Stream", annotated_frame)

        # Exit key listener
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_phone_detection()
