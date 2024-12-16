import json
import logging
import os

logger = logging.getLogger(__name__)

class ConfigManager:
    def __init__(self, config_file="config/config.json"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        try:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
            config_path = os.path.join(project_root, self.config_file)
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            return {}

    def get(self, key, default=None):
        return self.config.get(key, default)
