"""
Runs the Yolo Model
"""

from datetime import datetime
import time
import cv2
from dataclasses import dataclass
import numpy as np
from ultralytics.engine.results import Results
from ultralytics import YOLO
from threading import Thread

@dataclass
class DetectorFormat:
    model: str
    source: int | str

def generate_time_name(name: str):
    current_time = datetime.utcfromtimestamp(time.time())
    formatted_time = current_time.strftime("%m-%d-%H-%M-%S%f")
    return f'{name}_{formatted_time}.jpg'

class DetectorModel:
    """
    Runs the YOLO model and loops.
    """
    def __init__(self, hyperparams: DetectorFormat) -> None:
        self.annotated_frame = None
        self.model = YOLO(hyperparams.model)
        self.source = hyperparams.source
        self.results = None
        self.thread = Thread(target=self.loop_detection)
        self.thread.start()

    def get_annotate_frame(self) -> None | np.ndarray:
        """Gets the annotated frame in copied form."""
        if self.annotated_frame is None:
            return None
        return self.annotated_frame.copy()

    def loop_detection(self):
        """
        Main loop for the YOLO detection algorithm.
        Also generates annotated frame.
        Only sets the first result as the other detected items are not handled.
        """
        cam_feed = cv2.VideoCapture(self.source)
        while cam_feed.isOpened():
            ret, frame = cam_feed.read()
            if ret == False:
                continue
            # cv2.imwrite(generate_time_name('result'), frame)
            results: Results = self.model.predict(source=frame, verbose=False)
            self.annotated_frame = results[0].plot()
            self.set_result(results[0])

    def set_result(self, result: Results) -> None:
        self.results = result

    def get_result(self) -> None | Results:
        """Gets the result only once and reset it."""
        results = self.results
        self.results = None
        return results
