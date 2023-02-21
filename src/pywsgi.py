from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
from main import app
from core.config import config


http_server = WSGIServer(('', config.FLASK_HOST), app)
http_server.serve_forever()