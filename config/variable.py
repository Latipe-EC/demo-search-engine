import yaml


# singleton class to store global configuration
class GlobalConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(GlobalConfig, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        with open('C:\\Users\\Admin\\Code\\Python\\image-search-engine\\config\\config.yaml', 'r') as file:
            cfg = yaml.safe_load(file)
        self.config = cfg


global_cfg = GlobalConfig()

SERVER_PORT = global_cfg.config['server']['port']

RETRIEVAL_DB_IMAGE_FOLDER = global_cfg.config['retrieval_db']['image_folder']
RETRIVAL_DB_FEATURE_FOLDER = global_cfg.config['retrieval_db']['feature_folder']

MONGO_DB_CLIENT = global_cfg.config['mongodb']['uri']
