from domain.app import app
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

if __name__ == "__main__":
    http_server = WSGIServer(
        ("0.0.0.0", 8000), app, handler_class=WebSocketHandler
    )  # noqa: E501
    http_server.serve_forever()
