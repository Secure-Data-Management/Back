from server.keys.KeyManager import KeyManager
from os import environ, path
from dotenv import load_dotenv

PROJECT_ROOT = path.abspath(path.dirname(__file__))
load_dotenv(path.join(path.dirname(PROJECT_ROOT), '.env'))
PARAMS = environ.get('PARAMS')
G = environ.get('G')
assert PARAMS is not None and PARAMS != ""
assert G is not None and G != ""

KEY_MANAGER = KeyManager(PARAMS, G)
