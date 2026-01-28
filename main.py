from core.loggin import setup_logging
from core.server import make_server

setup_logging()

app = make_server()
