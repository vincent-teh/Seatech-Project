"""
Defines the configuration for the Serial controlling the Arduino.
"""

from abc import abstractmethod
from enum import Enum
import time
import serial


from typing import Any, Protocol
from threading import Thread
from flaskr.config import AlgoFormat, ConnectorFormat
from ultralytics.engine.results import Results


class ResultGenerator(Protocol):
    @abstractmethod
    def get_result(self) -> None | Results:
        """Obtained the detection result"""


class ServoState(Enum):
    bottom = '1'
    middle = '2'


class MovementAlgo:
    """
    Calculate the correct angle that needs to be turned by the robot. Directly
    dependent on detector for providing the results of detection.
    """
    def __init__(
        self, detector: ResultGenerator, hyperparams: AlgoFormat
        ) -> None:
        self.detector = detector
        self.y_correct = hyperparams.ycenter
        self.angle_factor = hyperparams.angle_factor

    def __call__(self):
        """Gets the correct angle to be turn based on the enum given."""
        result = self.detector.get_result()
        while result is None or len(result.boxes.xyxy) == 0:
            result = self.detector.get_result()
            time.sleep(0.1)
            continue
        boxes = result.boxes
        x1, y1, x2, y2 = self._unpack_xyxy(boxes.xyxy[0])
        y_center = (y1 + y2) / 2
        angle = (self.y_correct - y_center) / (2*self.y_correct)
        return angle

    def _unpack_xyxy(self, box):
        return int(box[0]), int(box[1]), int(box[2]), int(box[3])

class SerialConnector:
    def __init__(self, hyperparams: ConnectorFormat) -> None:
        self.ser = serial.Serial(hyperparams.port, hyperparams.baudrate)
        time.sleep(3)

    def listen(self) -> str:
        line = None
        while line is None:
            line = self.ser.readline().decode()
            time.sleep(0.2)
        return line

    def write(self, data: Any):
        """Sends data through serial."""
        data = str(data)
        self.ser.write(data.encode('utf-8'))


class ServosHandler:
    """
    Main loop running the servos handling logics.
    """
    def __init__(self, algo: MovementAlgo, ser: SerialConnector) -> None:
        self.algo = algo
        self.ser = ser
        self.thread = Thread(target=self.loop_servos)
        self.thread.start()

    def loop_servos(self):
        while True:
            # print("This line is run")
            # state = self.ser.listen()
            # print("This line is run")
            angle = self.algo()
            print(angle)
            self.ser.write(angle)
