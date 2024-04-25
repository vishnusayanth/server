import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = os.path.join(BASE_DIR, '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DEBUG_MODE = os.environ.get('DEBUG_MODE') == 'True'
LOCAL_DB = os.environ.get('LOCAL_DB') == 'True'
PRODUCTION = os.environ.get('PRODUCTION') == 'True'
ALLOWED_HOST = 'vishnusayanth-django-vishnusayanth-django.koyeb.app'
GITHUB_KEY = os.environ['GITHUB_KEY']
GITHUB_SECRET = os.environ['GITHUB_SECRET']
DJANGO_APP_KEY = os.environ['DJANGO_APP_KEY']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
NEWS_URL_TO_SCRAPE = "https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx1YlY4U0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen"
NEWS_LINK = 'https://news.google.com/'
ZOMATO_IFRAME_URL = 'https://www.zomato.com/widgets/res_search_widget.php?city_id=11772&language_id=1&theme=red&widgetType=large&sort=rating'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_SEARCH_URL = 'https://api.spotify.com/v1/search?q={0}&type={1}'
SPOTIFY_CATEGORIES_URL = 'https://api.spotify.com/v1/browse/categories'
SPOTIFY_PLAYLIST_URL = 'https://api.spotify.com/v1/browse/categories/{0}/playlists'
SPOTIFY_ID = os.environ['SPOTIFY_ID']
SPOTIFY_SECRET = os.environ['SPOTIFY_SECRET']
PASSWORD_COMPLEXITY = '''
    Your password must contain 7 characters, an alphabet and a number.
'''

