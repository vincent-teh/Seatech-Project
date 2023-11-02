"""
Defines the configuration for the Serial controlling the Arduino.
"""

from typing import Any, Protocol
import serial
from dataclasses import dataclass
from flaskr.detection import DetectorModel


@dataclass
class ConnectorFormat(Protocol):
    port: str
    baudrate: int


class MovementAlgo:
    def __init__(self, detector: DetectorModel, y_correct: float, angle_factor: float) -> None:
        """
        Args:
            detector (DetectorModel): Detector model in used.
            y_correct (float) : correct center point of the screen.
            angle_factor (float) : angle per pixel error
        """
        self.detector = detector
        self.y_correct = y_correct
        self.angle_factor = angle_factor

    def __call__(self):
        result = self.detector.get_result()
        if result is None:
            return None
        boxes = result.boxes
        x1, y1, x2, y2 = boxes.xyxy
        y_center = (y1 - y2) / 2
        y_error = self.y_correct - y_center
        return y_error * self.angle_factor


class SerialConnector:
    def __init__(self, port, baudrate) -> None:
        self.ser = serial.Serial(port, baudrate)

    def __call__(self, data: Any):
        data = str(data)
        self.ser.write(data.encode('utf-8'))


class ServosHandler:
    def __init__(self, algo: MovementAlgo, ser: SerialConnector) -> None:
        self.algo = algo
        self.ser = ser

    def loop_servos(self):
        while True:
            angle = self.algo()
            if angle is None:
                continue
            self.ser(angle)
