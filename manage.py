import os

from apps import app #create_app,db
from flask_script import Manager,Shell
from apps.models import Users
from apps.database import engine,db_session,Model

#app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app,engine=engine,db_session=db_session,Model=Model,Users=Users)
manager.add_command("shell",Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()