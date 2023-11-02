"""
Read the configuration from the YAML file and translate into appropriate datacless.
"""
import yaml
from flaskr.detection import DetectorFormat


class YamlParser:
    def __init__(self, path: str):
        with open(path) as file:
            self.configs = yaml.safe_load(file)

    def get_detector_config(self) -> DetectorFormat:
        return DetectorFormat(model=self.configs['model'],
                              source=self.configs['source'])
