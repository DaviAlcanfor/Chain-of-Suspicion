import json
from http.server import BaseHTTPRequestHandler, HTTPServer

PORTA = 8000


class Manipulador(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path != "/saude":
            self.send_error(404)
            return
        corpo = json.dumps({"status": "ok"}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", PORTA), Manipulador).serve_forever()
