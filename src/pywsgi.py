from __future__ import annotations

from core.config import config
from gevent import monkey
from gevent.pywsgi import WSGIServer
from main import app

monkey.patch_all()


http_server = WSGIServer(("", config.FLASK_HOST), app)
http_server.serve_forever()
