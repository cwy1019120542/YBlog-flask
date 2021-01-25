import os
from app.factory import create_app

config_type = os.getenv("CONFIG_TYPE", "product")
app = create_app(config_type)

if __name__ == "__main__":
    app.run()