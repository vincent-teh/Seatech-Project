"""
Defines the configuration for the Serial controlling the Arduino.
"""

from abc import abstractmethod
import time
import serial

from dataclasses import dataclass

from typing import Any, Protocol
from threading import Thread
from ultralytics.engine.results import Results


@dataclass
class AlgoFormat:
    ycenter: int
    angle_factor: int

@dataclass
class ConnectorFormat:
    port: str
    baudrate: int

class ResultGenerator(Protocol):
    @abstractmethod
    def get_result(self) -> None | Results:
        """Obtained the detection result"""


class ResultGen:
    @abstractmethod
    def get_result(self) -> None | Results:
        return None

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
        result = self.detector.get_result()
        if result is None:
            return None
        boxes = result.boxes
        x1, y1, x2, y2 = boxes.xyxy
        y_center = (y1 - y2) / 2
        y_error = self.y_correct - y_center
        return y_error * self.angle_factor


class SerialConnector:
    def __init__(self, hyperparams: ConnectorFormat) -> None:
        print("Contructor is Called")
        self.ser = serial.Serial(hyperparams.port, hyperparams.baudrate)
        time.sleep(3)

    def __call__(self, data: Any):
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
            angle = self.algo()
            if angle is None:
                continue
            self.ser(angle)


ser = ServosHandler(MovementAlgo(ResultGen(), AlgoFormat(100, 0.8)), SerialConnector(ConnectorFormat('COM6', 9600)))
