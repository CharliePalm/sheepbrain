from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from .request_handler import Handler
hostName = "localhost"
serverPort = 8080

handler = Handler()

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        result = handler.handle(self.path)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        result = handler.handle(self.path)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()