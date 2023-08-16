from domain.app import app
from gevent.pywsgi import WSGIServer

if __name__ == "__main__":
    http_server = WSGIServer(("127.0.0.1", 8000), app)
    http_server.serve_forever()
