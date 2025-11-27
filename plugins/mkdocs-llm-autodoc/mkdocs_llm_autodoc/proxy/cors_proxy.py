import os
import logging
import requests
from flask import Flask, request, Response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('cors-proxy')

app = Flask(__name__)

# Configuration from Environment Variables
TARGET_URL = os.environ.get("PROXY_TARGET_URL")
PORT = int(os.environ.get("PROXY_PORT", 8080))

if not TARGET_URL:
    logger.warning("PROXY_TARGET_URL not set. Proxy will not function correctly.")

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy(path):
    if request.method == 'OPTIONS':
        # Handle CORS preflight
        resp = Response()
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        return resp

    if not TARGET_URL:
        return Response("Proxy Error: PROXY_TARGET_URL not configured", status=500)

    # Construct target URL
    # Ensure no double slashes if TARGET_URL ends with / and path starts with /
    base = TARGET_URL.rstrip('/')
    url = f"{base}/{path}"
    
    logger.info(f"Proxying {request.method} {url}")

    # Forward headers (excluding host to avoid confusion)
    headers = {key: value for (key, value) in request.headers if key != 'Host'}

    try:
        # Forward request
        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            verify=True # Verify SSL of target
        )

        # Create response
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]

        response = Response(resp.content, resp.status_code, headers)
        
        # Add CORS headers to response
        response.headers['Access-Control-Allow-Origin'] = '*'
        
        return response

    except Exception as e:
        logger.error(f"Proxy error: {e}")
        return Response(f"Proxy Error: {e}", status=502)

if __name__ == '__main__':
    logger.info(f"Starting CORS Proxy on port {PORT} forwarding to {TARGET_URL}")
    app.run(host='0.0.0.0', port=PORT)
