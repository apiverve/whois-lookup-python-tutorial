"""
Calls APIVerve. Both the web app (app.py) and the command-line script use this,
so they read the key the same way and report errors the same way.

Set APIVERVE_API_KEY in .env (local) or in your Vercel project's environment variables.
Get a free key at https://dashboard.apiverve.com
"""
import os
import time
from pathlib import Path

import requests


def _load_env(path=Path(__file__).with_name('.env')):
    """Reads KEY=value lines from .env, without overriding variables that are already set."""
    if not path.exists():
        return
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"\''))


_load_env()


class ApiError(Exception):
    """An error with a message that is safe to show, and the HTTP status to send it with."""

    def __init__(self, message, status=502):
        super().__init__(message)
        self.status = status


def api_key():
    key = os.environ.get('APIVERVE_API_KEY', '').strip()
    if not key:
        raise ApiError('Missing APIVERVE_API_KEY. Add it to .env, or to your Vercel '
                       'project’s environment variables, then redeploy.', 500)
    return key


def call_api(api, params=None, json=None, files=None):
    """
    Calls an APIVerve API and returns its data, or raises ApiError with its message.
    Pass params for a GET, json for a JSON POST, or files for a file upload (a multipart POST).
    """
    url = f'https://api.apiverve.com/v1/{api}'
    headers = {'x-api-key': api_key()}
    try:
        if json is not None or files:
            res = requests.post(url, headers=headers, json=json, files=files, timeout=30)
        else:
            res = requests.get(url, headers=headers, params=params, timeout=30)
    except requests.RequestException:
        raise ApiError('Could not reach APIVerve. Try again in a moment.')

    try:
        body = res.json()
    except ValueError:
        body = None
    if not res.ok or not isinstance(body, dict) or body.get('status') != 'ok':
        err = (body or {}).get('error') if isinstance(body, dict) else None
        if isinstance(err, dict) and err.get('missing'):
            message = 'Missing: ' + ', '.join(err['missing'])
        elif isinstance(err, str) and err:
            message = err
        else:
            message = f'APIVerve returned {res.status_code}'
        raise ApiError(message, 429 if res.status_code == 429 else 502)
    return body['data']


# ============================================
# Rate limit (used by the web app)
# Once deployed, anyone who finds the URL can call it with YOUR key.
# This caps each visitor at RATE_LIMIT requests a minute. It is kept in
# memory, so it resets on cold starts and isn't shared between instances:
# good enough for a demo. For production, use a shared store (e.g. Upstash
# Redis) or put the app behind your own auth.
# ============================================
RATE_LIMIT = 10
WINDOW_SECONDS = 60
_hits = {}


def rate_limited(ip):
    now = time.monotonic()
    recent = [t for t in _hits.get(ip, []) if now - t < WINDOW_SECONDS]
    recent.append(now)
    _hits[ip] = recent
    if len(_hits) > 5000:
        _hits.clear()
    return len(recent) > RATE_LIMIT
