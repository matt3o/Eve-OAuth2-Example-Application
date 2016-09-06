from flask import Flask, url_for, session, request, jsonify, redirect
from flask_oauthlib.client import OAuth, OAuthResponse
from settings import DEBUG, SECRET_KEY, SQLALCHEMY_DATABASE_URI, CLIENT_ID, CLIENT_SECRET, HOST, PORT
from flask_session import Session
import redis

fapp = Flask(__name__)
fapp.config.from_pyfile('settings.py')
SESSION_REDIS = redis.StrictRedis(host='localhost', port=6379, db=0)
Session(fapp)

oauth = OAuth(fapp)
remote = oauth.remote_app(
    'remote',
    consumer_key=CLIENT_ID,
    consumer_secret=CLIENT_SECRET,
    request_token_params={'scope': 'email'},
    base_url='https://127.0.0.1:8000',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://127.0.0.1:8000/oauth/token',
    authorize_url='https://127.0.0.1:8000/oauth/authorize'
)


@fapp.route('/')
def index():
    if get('access_token'):
        resp = remote.get('api')
        if '_status' in resp.data and resp.data['_status'] == 'ERR':
            return redirect(url_for('refresh', callback=request.path))
        return jsonify(resp.data)
    return redirect(url_for('login'))


@fapp.route('/authorized')
def authorized():
    resp = remote.authorized_response()
    return parse_authorized_response(resp)


def parse_authorized_response(resp):
    print(type(resp))
    print(resp)
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, dict):
        session['access_token'] = (resp['access_token'], '')
        session['refresh_token'] = (resp['refresh_token'], '')
    elif isinstance(resp, OAuthResponse):
        print(resp.status)
        if resp.status != 200:
            session['access_token'] = None
            session['refresh_token'] = None
            return redirect(url_for('login'))
        else:
            session['access_token'] = (resp.data['access_token'], '')
            session['refresh_token'] = (resp.data['refresh_token'], '')
    else:
        raise Exception()
    return redirect('/')


@fapp.route('/login')
def login():
    return remote.authorize(callback=url_for('authorized', _external=True))


"""
Use the refresh token to get a new access token --> Currently just a reroute to login
"""


@fapp.route('/refresh/')
def refresh():
    callback = request.args.get("callback")
    data = {}
    data['grant_type'] = 'refresh_token'
    data['refresh_token'] = session['refresh_token'][0]
    data['client_id'] = CLIENT_ID
    data['client_secret'] = CLIENT_SECRET
    resp = remote.post(remote.access_token_url, data=data)

    parse_authorized_response(resp)

    if callback is not None:
        return redirect(callback)
    else:
        return redirect('/')


@fapp.route('/logout')
def logout():
    print('WARNING: This feature is broken because of a bug in oauthlib!')
    data = {}
    data['token'] = session.get('access_token')[0]
    remote.get(url='/oauth/revoke', data=data)
    session.pop('access_token', None)
    return redirect(url_for('index'))


@remote.tokengetter
def get_oauth_token():
    return session.get('access_token')


def set(key, value):
    session[key] = value


def get(key):
    return session.get(key, None)


# Create database connection object
import flask_db
from flask_mail import Mail

mail = Mail(fapp)

# Import all custom implemented controllers and routes
import flask_app.controller
