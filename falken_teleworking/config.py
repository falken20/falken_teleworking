# by Richi Rod AKA @richionline / falken20
# ./falken_teleworking/config.py

# Library that uses type annotation to validate data and manage settings.
from pydantic import BaseSettings
# Library to cache the data
from functools import lru_cache

__title__ = 'Falken Teleworking'
__version__ = '1.0.0'
__author__ = 'Falken'
__url_github__ = 'https://github.com/falken20/'
__url_twitter__ = 'https://twitter.com/richionline'
__url_linkedin__ = 'https://www.linkedin.com/in/richionline/'
__license__ = 'MIT License'
__copyright__ = '© 2023 by Richi Rod AKA @richionline / falken20'
__features__ = [
]


SETUP_DATA = {
    'title': __title__,
    'version': __version__,
    'author': __author__,
    'url_github': __url_github__,
    'url_twitter': __url_twitter__,
    'url_linkedin': __url_linkedin__,
    'license': __license__,
    'copyrigth': __copyright__,
    'features': __features__,
}


class Settings(BaseSettings):
    # pydantic will automatically assume those default values if it doesn’t
    # find the corresponding environment variables.
    env_name: str = "Local"
    base_url: str = "http://localhost:5000"
    # db_url: str = "sqlite:///./shortener.db"

    class Config:
        # When you add the Config class with the path to your env_file to your
        # settings, pydantic loads your environment variables from the .env file.
        env_file = ".env"
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings
