import os
from dotenv import load_dotenv

class ConfigLoader:
    def __new__(cls, dotenv_path):
        # Create a temporary instance
        instance = super(ConfigLoader, cls).__new__(cls)
        instance.config = {}
        instance.load_env(dotenv_path)
        return instance.config  # Return the config object directly

    def load_env(self, dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
        self.config[""] = os.getenv("my_id")
        self.config["my_password"] = os.getenv("my_password")

