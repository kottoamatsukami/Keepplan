from configparser import ConfigParser
import os

DEFAULT_CONFIG = {
    "Tree": {
        'save_path': './tree'
    }
}


class Config(object):
    def __init__(self, config_file: os.PathLike or str) -> None:
        self.config = ConfigParser()
        if os.path.exists(config_file):
            print(f"Loading config from {config_file}")
            self.config.read(config_file)
        else:
            print(f"Failed to find a config {config_file}")
            print(f"Using default config")
            self.config.read_dict(DEFAULT_CONFIG)
            with open(config_file, 'w') as file:
                self.config.write(file)

    def __getitem__(self, item):
        return self.config[item]
