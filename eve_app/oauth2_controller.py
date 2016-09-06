from flask import g, render_template, request, jsonify, make_response, redirect, session

from eve_app import eapp as app
from eve_app.eve_oauth2 import oauth, current_user
from sqldb import User
from sqldb import db
from flask_oauthlib.utils import extract_params


@app.before_request
def load_current_user():
    user = User.query.get(1)
    g.user = user


@app.route('/', methods=('GET', 'POST'))
def new_home():
    valid, req = oauth.verify_request(['email'])
    if valid:
        return jsonify(user=req.user.username)
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        session['id'] = user.id
        return redirect('https://127.0.0.1:5000/')
    user = current_user()
    return render_template('home.html', user=user)


@app.route('/oauth/token', methods=['POST', 'GET'])
@oauth.token_handler
def access_token():
    uri, http_method, body, headers = extract_params()
    print('#################### /oauth/token' + str(uri))
    print(headers)
    print(body)
    return {}


@app.route('/oauth/revoke', methods=['POST', 'GET'])
@oauth.revoke_handler
def revoke_token():
    pass


@app.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    # NOTICE: for real project, you need to require login
    if request.method == 'GET':
        # render a page for user to confirm the authorization
        return render_template('confirm.html')

    if request.method == 'HEAD':
        # if HEAD is supported properly, request parameters like
        # client_id should be validated the same way as for 'GET'
        response = make_response('', 200)
        response.headers['X-Client-ID'] = kwargs.get('client_id')
        return response

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'
