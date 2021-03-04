#!/usr/bin/python3
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import requests
import redis

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
CACHE_TIME = 60 * 60 * 24 * 7  # 1 week

# spawn redis connection
r = redis.Redis(host="redis", decode_responses=True)


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
    full_url = f"{url}/json"
    str_ip = f"{ip}"
    # see if this ip is in the cache
    c = r.hgetall(str_ip)
    if not c:
        # get it from the api
        print(f"Cache miss for {ip}")

        res = requests.get(f"{url}/org").text
        if res.upper() == 'GOOGLEWIFI':
            # Yes I know this is dumb
            res = f'STARLINK ( API says {res} )'
        # insert into the cache if the request is good
        if "error" in res:
            print(f"Skipping cache, got error: {res}")
        else:
            r.hmset(str_ip, {"value": res})
            r.expire(str_ip, CACHE_TIME)
        return res, full_url
    else:
        # use the cache
        print(f"Cache hit for {ip} - {c}")
        return c['value'], full_url


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
        elif self.path == f"/isp" or self.path == f"/org":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            o, url = org(ip)
            self.wfile.write(o.encode())


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class(('0.0.0.0', 8080), MyBaseHttpHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
