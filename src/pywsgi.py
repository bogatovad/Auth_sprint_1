from main import app
from core.config import config
from gevent.pywsgi import WSGIServer
from gevent import monkey

monkey.patch_all()


http_server = WSGIServer(('', config.FLASK_HOST), app)
http_server.serve_forever()
