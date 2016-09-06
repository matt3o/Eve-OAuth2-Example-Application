MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = ''
MONGO_PASSWORD = ''
MONGO_DBNAME = 'api'

APP_NAME = 'Eve API'
URL_PREFIX = 'api'

SECRET_KEY = '12j3oiu98dasufdasoiufasmnhklasdftemp34lkadsfds'

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
DEBUG = True

SENTINEL_MANAGEMENT_USERNAME = 'admin'
SENTINEL_MANAGEMENT_PASSWORD = 'kj.<zxcvklj<p}poooipqwef,das.f09123nkjaz'
SQLALCHEMY_DATABASE_URI = 'mysql://root:Test123@localhost/todo_oauth2?charset=utf8'

people = {
    'item_title': 'person',
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'id',
    },
    'schema': {
        'id': {
            'type': 'int',
            'required': True,
            'unique': True,
        },
        'email': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 15,
            'required': True,
            'unique': True,
            'empty': False,
            'is_email': True
        },
        'password': {
            'type': 'string'
        }
    }
}

todos = {
    'schema': {
        'id': {
            'type': 'string',
            'unique': True,
            'required': True,
        },
        'user': {
            'data_relation': {
                'resource': 'people',
                'field': 'id'
            }
        }

    }
}

DOMAIN = {
    'people': people,
}
