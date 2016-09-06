APP_NAME = 'Todo'

HOST = '0.0.0.0'
PORT = 5000

CLIENT_ID = 'dev'
CLIENT_SECRET = 'dev'

# SQLALCHEMY
SQLALCHEMY_DATABASE_URI = 'mysql://root:Test123@localhost/todo_oauth2?charset=utf8'

# FLASK SECURITY
# URL_PREFIX='api'
SECRET_KEY = '12j3oiu98dasufdasoiufasmnhklasdftemp34lkadsfds'
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = 'A0B4LlwZhaQ!Sbw4(ef1vY!pxrk_KJk&^KtecX0RMaMdEtVQyrbbi5OWQf!)WaRE'
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True

# FLASK MAIL
# After 'Create app'
MAIL_SERVER = '127.0.0.1'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'

DEBUG = True

OAUTH_CLIENT_ID = 'FxlY88EI8lhzRuqmliLXSyUKUoSaabyvbol4vxle'
SESSION_TYPE = 'redis'
SESSION_COOKIE_SECURE = True
SESSION_USE_SIGNER = True