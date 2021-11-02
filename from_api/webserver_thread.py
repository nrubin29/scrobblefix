from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from typing import Optional

result: Optional[str]


class WebserverThread(Thread):
    result: Optional[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = None

    def run(self):
        global result

        class MyServer(BaseHTTPRequestHandler):
            def do_GET(self):
                global result
                result = self.path

        webserver = HTTPServer(('localhost', 8080), MyServer)

        try:
            webserver.handle_request()
        except KeyboardInterrupt:
            pass

        self.result = result

    def join(self, *args, **kwargs) -> Optional[str]:
        super().join(*args, **kwargs)
        return self.result
