from flask import Flask
from config import Config
from elastic_app_search import Client

app = Flask(__name__)
app.config.from_object(Config)


def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
        raise ValueError("Cannot covert {} to a bool".format(s))


bool_value = str_to_bool(app.config['APP_SEARCH_USE_HTTPS'])

client_app_search = Client(
    api_key=app.config['APP_SEARCH_API_KEY'],
    base_endpoint=app.config['APP_SEARCH_BASE_ENDPOINT'],
    use_https=bool_value
)

client_blog_search = Client(
    api_key=app.config['APP_SEARCH_API_KEY_BLOG'],
    base_endpoint=app.config['APP_SEARCH_BASE_ENDPOINT'],
    use_https=bool_value
)

from app import routes
