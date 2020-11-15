from server.keys.KeyManager import KeyManager
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
PARAMS = environ.get('PARAMS')
G = environ.get('G')
KEY_MANAGER = KeyManager(PARAMS, G)
