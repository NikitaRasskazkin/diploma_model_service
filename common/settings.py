"""Global project settings"""
import os

from pathlib import Path
from dotenv import dotenv_values


if os.environ.get('VARIABLES_INITIALIZED'):
    PORT = int(os.environ.get('PORT'))
    DEBUG = bool(int(os.environ.get('DEBUG')))
else:
    config = dotenv_values(".env.developer")
    PORT = int(config.get('PORT', 5000))
    DEBUG = bool(int(config.get('DEBUG', True)))

BASE_DIR = Path(__file__).resolve().parent.parent

URLS_ROOT = '/api/v1.0'
