from flask import Flask, render_template, Response, jsonify
import cv2
from ultralytics import YOLO
import time
import os
import threading

app = Flask(__name__)

# Global variables for detection data
latest_detections = []
detection_lock = threading.Lock()

# Model and Camera Configuration
# Paths below resolve against the repository layout, not the current
# working directory, so the server can be started from anywhere.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.dirname(BASE_DIR)  # the repository's model/ directory
MODEL_PATH = os.environ.get('MODEL_PATH')
if not MODEL_PATH:
    MODEL_PATH = os.path.join(MODEL_DIR, 'best_ncnn_model')
    if not os.path.exists(MODEL_PATH):
        MODEL_PATH = os.path.join(MODEL_DIR, 'best.pt')

# IP camera stream endpoint; override with CAMERA_SOURCE ('0' = default webcam).
CAMERA_SOURCE = os.environ.get('CAMERA_SOURCE', 'http://192.168.1.100:8080/video')
if CAMERA_SOURCE.isdigit():
    CAMERA_SOURCE = int(CAMERA_SOURCE)

# Load Model
try:
    model = YOLO(MODEL_PATH, task='detect')
    print(f"Model loaded: {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def generate_frames():
    global latest_detections
    cap = cv2.VideoCapture(CAMERA_SOURCE)
    
    # Fallback to local webcam if IP camera fails
    if not cap.isOpened():
        print("Warning: Could not open IP camera, falling back to local webcam (0)")
        cap = cv2.VideoCapture(0)

    prev_time = 0
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        # Inference
        if model:
            results = model.predict(source=frame, imgsz=320, conf=0.4, verbose=False, stream=True)
            
            new_detections = []
            for r in results:
                frame = r.plot() # Get annotated frame
                
                # Extract detection info for the log
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    label = r.names[cls_id]
                    conf = float(box.conf[0])
                    new_detections.append({'label': label, 'confidence': conf})
            
            with detection_lock:
                latest_detections = new_detections

        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detections')
def get_detections():
    with detection_lock:
        return jsonify(latest_detections)

if __name__ == '__main__':
    # host='0.0.0.0' allows access from other devices in the network
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', '5000'))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ('1', 'true', 'yes')
    app.run(host=host, port=port, debug=debug, threaded=True)
