#!/usr/bin/python3
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests


def gen(ip, org, url):
    return f"""
    <html>
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
        res = 'STARLINK'
    return res, f"{url}/json"


class MyBaseHttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            ip = self.address_string()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            o, url = org(ip)
            print(f"Request from: {ip}, location: {o}, full url: {url}")
            self.wfile.write(gen(ip, o, url).encode())


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class(('0.0.0.0', 8888), MyBaseHttpHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
