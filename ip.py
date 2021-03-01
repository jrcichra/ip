#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import time


def gen(ip):
    return f"""
    <html>
    <head>
    </head>
    <body>
        <h1>{ip}</h1>
    </body>
    </html>
    """


class MyBaseHttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(gen(self.address_string()).encode())


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class(('0.0.0.0', 8888), MyBaseHttpHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
