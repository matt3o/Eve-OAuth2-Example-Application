from flask_app import fapp
from werkzeug.serving import run_simple
import os

if __name__ == '__main__':
    os.environ["SSL_CERT_FILE"] = "certs/cert.pem"
    context = ('certs/cert.pem', 'certs/key.pem')
    run_simple('0.0.0.0', 5000, fapp, use_reloader=True, use_debugger=True, ssl_context=context)
