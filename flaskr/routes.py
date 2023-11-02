import cv2
import flask

from flaskr.extensions import main, detector


@main.route('/')
def create_main_page():
    return flask.render_template('base.html')

@main.route('/annotated_img')
def show_annotated_img():
    def gen_frame():
        while True:
            if detector.annotated_frame is not None:
                frame = detector.annotated_frame
                frame = cv2.imencode('.jpg', frame)[1].tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                pass
    return flask.Response(
        gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
