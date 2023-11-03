"""
Instantiates all required high level controller.
"""
from flask import Blueprint
from flaskr.config import YamlParser
from flaskr.controller import MovementAlgo, SerialConnector, ServosHandler
from flaskr.detection import DetectorModel


configs = YamlParser(path="C:\\YuSheng\\Study\\Seatech-Project\\config.yaml")
detector = DetectorModel(configs.get_detector_config())
servos = ServosHandler(
    algo=MovementAlgo(detector, configs.get_algo_config()),
    ser=SerialConnector(configs.get_controller_config()))
main = Blueprint("main", __name__)
