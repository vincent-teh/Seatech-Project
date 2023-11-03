"""
Read the configuration from the YAML file and translate into appropriate datacless.
"""

from dataclasses import dataclass
import yaml
from flaskr.detection import DetectorFormat


@dataclass
class AlgoFormat:
    ycenter: int
    angle_factor: int


@dataclass
class ConnectorFormat:
    port: str
    baudrate: int


class YamlParser:
    def __init__(self, path: str):
        with open(path) as file:
            self.configs = yaml.safe_load(file)

    def get_detector_config(self) -> DetectorFormat:
        return DetectorFormat(model=self.configs['model'],
                              source=self.configs['source'])

    def get_controller_config(self) -> ConnectorFormat:
        return ConnectorFormat(port=self.configs['port'],
                               baudrate=self.configs['baudrate'])

    def get_algo_config(self) -> AlgoFormat:
        return AlgoFormat(ycenter=self.configs['ycenter'],
                          angle_factor=self.configs['angle_factor'])
