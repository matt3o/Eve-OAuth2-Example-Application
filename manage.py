from flask_script import Manager

import traceback
import sys

from eve_app import eapp
from sqldb import db, User, Token, Client

manager = Manager(eapp)


@manager.command
def prefill_database():
    """Prefill the database with some default values including the currently
    hardcoded client_id and client_secret values
    """
    db.create_all()
    db.session.commit()

    client1 = Client(
        name='dev', client_id='dev', client_secret='dev',
        _redirect_uris=(
            'https://localhost:5000/authorized '
            'https://127.0.0.1:5000/authorized '
            'https://localhost/authorized'
        ),
    )

    client2 = Client(
        name='confidential', client_id='confidential',
        client_secret='confidential', client_type='confidential',
        _redirect_uris=(
            'https://localhost:5000/authorized '
            'https://127.0.0.1:5000/authorized '
            'https://localhost/authorized'
        ),
    )

    user = User(username='admin')

    access_token = Token(
        user_id=1, client_id='dev', access_token='expired', expires_in=0
    )

    try:
        db.session.add(client1)
        db.session.add(client2)
        db.session.add(user)
        db.session.add(access_token)
        db.session.commit()
    except:
        print("Warning: Some SQL Operations have failed. Please review the stack trace and fix it!")
        traceback.print_exc(file=sys.stdout)
        db.session.rollback()

@manager.command
def delete_token():
    user = User.query.filter_by(username='admin').first()
    token = Token.query.filter_by(user_id=user.id).first()
    # Modifying the admins token value so that the client no longer knows it.
    token.access_token='expired'
    token.refresh_token='expired'
    db.session.add(token)
    db.session.commit()




if __name__ == "__main__":
    manager.run()
