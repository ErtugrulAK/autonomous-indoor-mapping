import cv2
from ultralytics import YOLO

def start_detection():
    # 1. Load Object Detection Model
    try:
        model = YOLO('best.pt') 
        print("Trained model weight file ('best.pt') loaded successfully.")
    except Exception:
        print("WARNING: 'best.pt' not found. Loading fallback baseline model ('yolov8n.pt')...")
        model = YOLO('yolov8n.pt')

    # 2. Initialize Default Camera Device (Index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Unable to open video capture device 0.")
        return

    print("Local camera initialized. Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform inference with confidence threshold 0.5
        results = model(frame, conf=0.5)

        # Draw bounding boxes and labels
        annotated_frame = results[0].plot()

        # Display output stream
        cv2.imshow("Robot Vision - Local Camera", annotated_frame)

        # Terminate stream on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_detection()
