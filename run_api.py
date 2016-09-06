from eve_app import eapp
from werkzeug.serving import run_simple
import logging

logger = logging.getLogger('oauthlib')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

if __name__ == '__main__':
    context = ('certs/cert.pem', 'certs/key.pem')
    run_simple('0.0.0.0', 8000, eapp, use_reloader=True, use_debugger=True, ssl_context=context)
