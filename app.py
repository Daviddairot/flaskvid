from flask import Flask, Response
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    # Render a template with a button to request camera permission
    return render_template('ind.html')

def generate_frames():
    camera = cv2.VideoCapture(0)  # Open the webcam (camera index 0)
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()

@app.route('/video_feed/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

