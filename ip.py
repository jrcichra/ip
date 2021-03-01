#!/usr/bin/python3
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import requests

BASE_PATH = os.path.dirname(os.path.realpath(__file__))


def gen(ip, org, url):
    return f"""
    <html>
    <title>{ip}</title>
    <head>
    </head>
    <body>
        <h1>{ip}</h1>
        <h2>{org}</h2>
        <p> Source: <a target="_blank" href="{url}">{url}</a> </p>
    </body>
    </html>
    """


def org(ip):
    url = f"https://ipapi.co/{ip}"
    res = requests.get(f"{url}/org").text
    if res.upper() == 'GOOGLEWIFI':
        # Yes I know this is dumb
        res = f'STARLINK ( API says {res} )'
    return res, f"{url}/json"


class MyBaseHttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        ip = self.address_string()
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            o, url = org(ip)
            print(f"Request from: {ip}, location: {o}, full url: {url}")
            self.wfile.write(gen(ip, o, url).encode())
        elif self.path == f"/favicon.ico":
            self.send_response(200)
            self.send_header('Content-type', 'image/x-icon')
            self.end_headers()
            with open(f'{BASE_PATH}/favicon.ico', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == f"/ip":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(ip.encode())
        elif self.path == f"/org":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            o, url = org(ip)
            self.wfile.write(o.encode())


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class(('0.0.0.0', 8888), MyBaseHttpHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
