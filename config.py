import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    APP_SEARCH_API_KEY = os.environ.get('APP_SEARCH_API_KEY')
    APP_SEARCH_API_KEY_BLOG = os.environ.get('APP_SEARCH_API_KEY_BLOG')
    APP_SEARCH_BASE_ENDPOINT = os.environ.get('APP_SEARCH_BASE_ENDPOINT') or 'localhost:3002/api/as/v1'
    APP_SEARCH_USE_HTTPS = os.environ.get('APP_SEARCH_USE_HTTPS') or 'False'
    # APP_SEARCH_USE_HTTPS = False or False
    POSTS_PER_PAGE = int(os.environ.get('APP_SEARCH_DOCS_PER_PAGE')) or 10
