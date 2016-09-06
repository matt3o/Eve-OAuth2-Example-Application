from flask import g
from flask_oauthlib.provider import OAuth2Provider
from flask import jsonify, session
from flask_oauthlib.contrib.oauth2 import bind_cache_grant
from flask_oauthlib.contrib.oauth2 import bind_sqlalchemy
import werkzeug
from eve.auth import TokenAuth
from datetime import datetime, timedelta
from sqldb import db, User, Token, Client
import logging
from flask_oauthlib.utils import extract_params

oauth = OAuth2Provider()
logger = logging.getLogger('todo/eve_app')


def current_user():
    return g.user


class EveOAuth2(TokenAuth):
    def __init__(self):
        super(EveOAuth2, self).__init__()

    def check_auth(self, token, allowed_roles, resource, method):
        logger.debug("check_auth(self, token, allowed_roles, resource, method)")
        valid, req = oauth.verify_request(['email'])
        uri, http_method, body, headers = extract_params()
        logger.debug(session)
        logger.debug(headers)
        if valid:
            logger.debug('### valid ###' + str(req.user.username))
            return True
        else:
            logger.debug('### not valid ### ' + req.error_message)
            raise werkzeug.exceptions.Unauthorized(description=req.error_message)

    def authorized(self, allowed_roles, resource, method):
        return self.check_auth("", allowed_roles, resource, method)


def cache_provider(app):
    bind_sqlalchemy(oauth, db.session, user=User,
                    token=Token, client=Client)

    app.config.update({'OAUTH2_CACHE_TYPE': 'simple'})
    bind_cache_grant(app, oauth, current_user)
    return oauth


def create_server(app):
    with app.app_context():
        db.init_app(app)

        oauth.init_app(app)
        cache_provider(app)
        from eve_app.oauth2_controller import *


@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    logger.debug('oauth.tokengetter')
    logger.debug(access_token)
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()
    else:
        try:
            token = session['remote_oauth'][0]
            return Token.query.filter_by(access_token=token).first()
        except:
            pass
    return None


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(
        client_id=request.client.client_id,
        user_id=request.user.id
    )
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)

    expires_in = token.pop('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    db.session.add(tok)
    db.session.commit()
    return tok


@oauth.invalid_response
def invalid_require_oauth(req):
    return jsonify(message=req.error_message), 401


@oauth.usergetter
def get_user(username, password, client, request, *args, **kwargs):
    # client: current request client
    if not client.has_password_credential_permission:
        return None
    user = User.get_user_by_username(username)
    if not user.validate_password(password):
        return None
    # parameter `request` is an OAuthlib Request object.
    # maybe you will need it somewhere
    return user
