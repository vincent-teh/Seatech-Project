"""
Runs the Yolo Model
"""

import cv2
from typing import Any, Protocol
from dataclasses import dataclass
from ultralytics.engine.results import Results
from ultralytics import YOLO
from threading import Thread

@dataclass
class DetectorFormat(Protocol):
    model: str
    source: int


class DetectorModel:
    def __init__(self, hyperparams: DetectorFormat) -> None:
        self.annotated_frame = None
        self.model = YOLO(hyperparams.model)
        self.source = hyperparams.source
        self.thread = Thread(target=self.loop_detection)
        self.thread.start()

    def loop_detection(self):
        cam_feed = cv2.VideoCapture(self.source)
        while True:
            ret, frame = cam_feed.read()
            if frame is None:
                continue
            self.results: Results = self.model.predict(source=frame)
            self.annotated_frame = self.results[0].plot()
                # frame = cv2.imencode('.jpg', annotated_frame)[1].tobytes()
            # if frame is not None:
            #     yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # Process results list
        # for result in results:
        #     boxes = result.boxes  # Boxes object for bbox outputs
        #     masks = result.masks  # Masks object for segmentation masks outputs
        #     keypoints = result.keypoints  # Keypoints object for pose outputs
        #     probs = result.probs  # Probs object for classification outputs
