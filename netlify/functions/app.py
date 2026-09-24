import os
import sys

# Ensure project root is in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import serverless_wsgi
from app import create_app

# Instantiate the Flask application
flask_app = create_app()

def handler(event, context):
    """
    AWS Lambda / Netlify Functions handler for the Flask application.
    Translates Netlify serverless HTTP events into WSGI requests.
    """
    # Clean URL path if Netlify forwards internal function route
    path = event.get('path', '/')
    prefix = '/.netlify/functions/app'
    if path.startswith(prefix):
        cleaned_path = path[len(prefix):]
        if not cleaned_path or not cleaned_path.startswith('/'):
            cleaned_path = '/' + cleaned_path
        event['path'] = cleaned_path

    return serverless_wsgi.handle_request(flask_app, event, context)
