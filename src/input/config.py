import yaml

class Config:
    """Singleton config object."""
    
    config = None
    
    @staticmethod
    def set_from_file(filename):
        if Config.config is not None:
            raise Exception
        with open(filename, "r", encoding="utf-8") as f:
            config_dict = yaml.safe_load(f)
            Config.config = config_dict

    @staticmethod
    def get_config():
        if Config.config is None:
            raise Exception
        return Config.config
