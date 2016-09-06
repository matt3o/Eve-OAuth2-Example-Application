# Simple Eve (/Flask) API protected by OAuth2 

using the Authorization Code flow (Server + Client provided).
The Flask Client tries to fetch some data from an Eve Rest API. Before he can do so he has 
So far there is no example project on Flask / Eve using the OAuth2 Authorization Code Flow.
This project aims to close this gap and to show how this can be done.
If anybody is up to adding some functionality I surely will integrate it in the project.
Hope this project is useful to anyone else out there - if you have any questions just open an issue.
Thanks to [Flask Oauthlib](https://github.com/lepture/flask-oauthlib) for making this possible. This is based on their example code which can be found [here](https://github.com/lepture/flask-oauthlib/tree/master/tests/oauth2).

Note: *This approach does not only work for Eve but also for Flask as those are very similar.
This project is WiP. While some things may work well others do not work at all.*

## How to start
Make sure you have MySQL installed on your PC. Then modify the database settings in flask_app/settings.py and eve_app/settings.py.
`SQLALCHEMY_DATABASE_URI = 'mysql://root:Test123@localhost/todo_oauth2?charset=utf8'`

Now prefill the database and create the tables by running
`python manage.py prefill_database`

Then generate yourself a self-signed certificate so all communication is done over SSL:
`mkdir certs && openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 1000 -nodes -subj "/C=DE/ST=None/L=None/O=None/OU=Org/CN=127.0.0.1"`
*Note: Accessing the server via http will not work!*
l
And this concludes the setup - start the API and the client:
```
# Start the api in one terminal window
python run_api.py
# start the flask application in another terminal
SSL_CERT_FILE=certs/cert.pem python run.py
```
And open your webbrowser at https://127.0.0.1:5000 and the OAuth2 flow should begin. 

## Other useful information
 
 - [x] OAuth2 Token are stored securely in an Server Side Session Object.
 - [x] Token autofreshing is implemented
 - [x] SSL Protection is activated
 - [x] using flask_import instead of flask.ext.import
 - [x] Logging is working - even though it could still be enhanced
 
 - [ ] Token revokation does not work because of a bug in the underlying lib (look into the flask oauthlib issue for more information)
 - [ ] Remember to change any kind of secure tokens in the settings before actually using this!!!
 - [ ] No authorization is implemented so far.
 - [ ] The state parameter is neither used nor checked which means the flow open to CSRF attacks.
