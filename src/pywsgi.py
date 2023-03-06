from gevent import monkey
from gevent.pywsgi import WSGIServer

monkey.patch_all()

from core.config import config
from main import app


http_server = WSGIServer(('', config.FLASK_HOST), app)
http_server.serve_forever()
