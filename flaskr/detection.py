"""
Runs the Yolo Model
"""

import cv2
from typing import Any, Protocol
from dataclasses import dataclass
import numpy as np
from ultralytics.engine.results import Results
from ultralytics import YOLO
from threading import Thread

@dataclass
class DetectorFormat:
    model: str
    source: int | str


class DetectorModel:
    def __init__(self, hyperparams: DetectorFormat) -> None:
        self.annotated_frame = None
        self.model = YOLO(hyperparams.model)
        self.source = hyperparams.source
        self.thread = Thread(target=self.loop_detection)
        self.thread.start()

    def get_annotate_frame(self) -> None | np.ndarray:
        if self.annotated_frame is None:
            return None
        return self.annotated_frame.copy()

    def loop_detection(self):
        cam_feed = cv2.VideoCapture(self.source)
        while cam_feed.isOpened():
            ret, frame = cam_feed.read()
            if ret == False:
                continue
            self.results: Results = self.model.predict(source=frame, verbose=False)
            self.annotated_frame = self.results[0].plot()

        # Process results list
        # for result in results:
        #     boxes = result.boxes  # Boxes object for bbox outputs
        #     masks = result.masks  # Masks object for segmentation masks outputs
        #     keypoints = result.keypoints  # Keypoints object for pose outputs
        #     probs = result.probs  # Probs object for classification outputs
