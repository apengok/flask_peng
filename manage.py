import os

from apps import app,db #create_app,db
from flask_script import Manager,Shell

#no matter the models where is,just import here
#they can processed by migrate
from apps.models import Users,Role
from apps.models.blogs import BlogPost,Category,Tag,Comments
#from apps.database import engine,db_session,Model
from flask_migrate import Migrate,MigrateCommand

#app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

DATABASE_URI = getattr(app.config, 'SQLALCHEMY_DATABASE_URI', '')
is_sqlite = DATABASE_URI.startswith('sqlite:')

migrate = Migrate(app,db)
#migrate.init_app(app, db, render_as_batch=is_sqlite)

def make_shell_context():
    return dict(app=app,db=db,Users=Users,Role=Role,BlogPost=BlogPost,Category=Category,Tag=Tag,Comments=Comments)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()