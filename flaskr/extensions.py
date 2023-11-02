"""
Instantiates all required high level controller.
"""

from dataclasses import dataclass
from flask import Blueprint
from flaskr.detection import DetectorModel


@dataclass
class DetectorFormat:
    model: str
    source: int

main = Blueprint("main", __name__)
detector = DetectorModel(DetectorFormat(model="yolov8s.pt", source=0,))
