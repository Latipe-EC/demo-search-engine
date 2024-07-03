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
        with open('./config/config.yaml', 'r') as file:
            cfg = yaml.safe_load(file)
        self.config = cfg


# global configuration
global_cfg = GlobalConfig()

SERVER_PORT = global_cfg.config['server']['port']

RETRIEVAL_DB_IMAGE_FOLDER = global_cfg.config['retrieval_db']['image_folder']
RETRIVAL_DB_FEATURE_FOLDER = global_cfg.config['retrieval_db']['feature_folder']

MONGO_DB_CLIENT = global_cfg.config['mongodb']['uri']

RABBITMQ_HOST = global_cfg.config['rabbitmq']['host']
PRODUCT_UPDATES_QUEUE = global_cfg.config['rabbitmq']['queue_name']
PRODUCT_EXCHANGE = global_cfg.config['rabbitmq']['exchange_name']
PRODUCT_ROUTING_KEY = global_cfg.config['rabbitmq']['routing_key']
X_API_KEY = global_cfg.config['x_api_key']
PRODUCT_SERVICE_URL = global_cfg.config['product_service_url']