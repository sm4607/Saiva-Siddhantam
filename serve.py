#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""உள்ளூர் சேவையகம் — Local preview server.

Usage / பயன்பாடு:
    python3 serve.py            # http://localhost:8000
    python3 serve.py 8080       # வேறு துறை

Run this from the repository folder, then open the address it prints.
Ctrl+C to stop.
"""

import http.server
import os
import socketserver
import sys
import webbrowser

os.chdir(os.path.dirname(os.path.abspath(__file__)))

port = 8000
if len(sys.argv) > 1:
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Port must be a number, e.g. python3 serve.py 8080")
        sys.exit(1)


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = dict(
        http.server.SimpleHTTPRequestHandler.extensions_map,
        **{
            ".html": "text/html; charset=utf-8",
            ".md": "text/markdown; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".svg": "image/svg+xml",
        }
    )

    def end_headers(self):
        # Always serve fresh files while editing.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


socketserver.TCPServer.allow_reuse_address = True

for attempt in range(10):
    try:
        httpd = socketserver.TCPServer(("", port), Handler)
        break
    except OSError:
        port += 1
else:
    print("துறைகள் எதுவும் கிடைக்கவில்லை. வேறு துறையைக் குறிப்பிடவும்.")
    sys.exit(1)

url = "http://localhost:%d/" % port
print("")
print("  சைவ சித்தாந்தம் — உள்ளூர் சேவையகம்")
print("  " + url)
print("")
print("  நிறுத்த: Ctrl + C")
print("")

try:
    webbrowser.open(url)
except Exception:
    pass

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\n  நிறுத்தப்பட்டது.")
    httpd.server_close()
