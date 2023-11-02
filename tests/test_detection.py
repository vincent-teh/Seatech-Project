from test_init import init_test
init_test()

from detection import DetectorModel
from dataclasses import dataclass


@dataclass
class TestDetector():
    model: str
    source: int


if __name__ == "__main__":
    detector = DetectorModel(TestDetector(model="yolov8s.pt", source=0))
    detector()