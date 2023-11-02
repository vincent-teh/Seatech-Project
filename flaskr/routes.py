from time import sleep
import flask
import cv2

from flaskr.extensions import main, detector

@main.route('/')
def create_main_page():
    return flask.render_template('base.html')

@main.route('/annotated_img')
def show_annotated_img():
    def gen_frames():
        while True:
            frame = detector.get_annotate_frame()  # read the camera frame
            if frame is None:
                sleep(0.2)
                continue
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
    return flask.Response(
        gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
