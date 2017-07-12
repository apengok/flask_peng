import os

from apps import app,db #create_app,db
from flask_script import Manager,Shell

#no matter the models where is,just import here
#they can processed by migrate
from apps.models import Users
from apps.models.blogs import BlogPost,Keyword
#from apps.database import engine,db_session,Model
from flask_migrate import Migrate,MigrateCommand

#app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

migrate = Migrate(app,db)


def make_shell_context():
    return dict(app=app,db=db,Users=Users)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()