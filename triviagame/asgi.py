"""
ASGI entrypoint file for default channel layer.
Points to the channel layer configured as "default" so you can point
ASGI applications at "liveblog.asgi:channel_layer" as their channel layer.
"""

import os
from channels.asgi import get_channel_layer
import dotenv

dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "triviagame.settings")
channel_layer = get_channel_layer()