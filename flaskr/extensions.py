"""
Instantiates all required high level controller.
"""
from flask import Blueprint
from flaskr.detection import DetectorModel
from flaskr.config import YamlParser

configs = YamlParser(path="C:\\YuSheng\\Study\\Seatech-Project\\config.yaml")
detector = DetectorModel(configs.get_detector_config())
main = Blueprint("main", __name__)
