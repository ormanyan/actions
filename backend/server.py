"""Tiny stdlib-only JSON API: serves random DevOps quotes."""
import json
import os
import random
from http.server import HTTPServer, BaseHTTPRequestHandler

QUOTES = [
    {"text": "It works on my machine.", "author": "Every developer, ever"},
    {"text": "There is no cloud, it's just someone else's computer.", "author": "Unknown"},
    {"text": "Simplicity is a prerequisite for reliability.", "author": "Edsger W. Dijkstra"},
    {"text": "Hope is not a strategy.", "author": "SRE proverb"},
    {"text": "You build it, you run it.", "author": "Werner Vogels"},
    {"text": "Everything fails, all the time.", "author": "Werner Vogels"},
    {"text": "If it hurts, do it more often.", "author": "Martin Fowler"},
    {"text": "Automate all the things!", "author": "DevOps proverb"},
    {"text": "The best error message is the one that never shows up.", "author": "Thomas Fuchs"},
    {"text": "Weeks of coding can save you hours of planning.", "author": "Unknown"},
    {"text": "kubectl delete pod is my love language.", "author": "Anonymous SRE"},
    {"text": "First, solve the problem. Then, write the code.", "author": "John Johnson"},
]

POD_NAME = os.environ.get("HOSTNAME", "unknown")
hits = 0

class Handler(BaseHTTPRequestHandler):
    def _json(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        global hits
        if self.path == "/api/quote":
            hits += 1
            quote = random.choice(QUOTES)
            self._json(200, {
                "quote": quote["text"],
                "author": quote["author"],
                "pod": POD_NAME,
                "hits": hits,
            })
        elif self.path == "/api/health":
            self._json(200, {"status": "ok", "pod": POD_NAME})
        else:
            self._json(404, {"error": "not found"})

    def log_message(self, *args):
        pass  # keep pod logs quiet

print(f"Backend listening on :8000 (pod: {POD_NAME})", flush=True)
HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
