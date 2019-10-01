from flask import Flask
from config import Config
from elastic_app_search import Client

app = Flask(__name__)
app.config.from_object(Config)

client_app_search = Client(
    api_key=app.config['APP_SEARCH_API_KEY'],
    base_endpoint=app.config['APP_SEARCH_BASE_ENDPOINT'],
    use_https=app.config['APP_SEARCH_USE_HTTPS']
)

client_blog_search = Client(
    api_key=app.config['APP_SEARCH_API_KEY_BLOG'],
    base_endpoint=app.config['APP_SEARCH_BASE_ENDPOINT'],
    use_https=app.config['APP_SEARCH_USE_HTTPS']
)

from app import routes
