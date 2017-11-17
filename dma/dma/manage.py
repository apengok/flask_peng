import os

from apps import app,db #create_app,db
from flask_script import Manager,Shell

#no matter the models where is,just import here
#they can processed by migrate
from apps.models import WBalance
#from apps.database import engine,db_session,Model
from flask_migrate import Migrate,MigrateCommand

#app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

DATABASE_URI = getattr(app.config, 'SQLALCHEMY_DATABASE_URI', '')
is_sqlite = DATABASE_URI.startswith('sqlite:')

migrate = Migrate(app,db)
#migrate.init_app(app, db, render_as_batch=is_sqlite)

def make_shell_context():
    return dict(app=app,db=db,WBalance=WBalance)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

@manager.command
def init_wbalance():
    import random
    month = ['Jan','Feb','Mar','Apr', 'May', 'June', 'July', 'Aug', 'Sept',  'Nov', 'Dec']
    for mon in month:
        name = mon
        totoal_in=random.randint(210000,250000)
        auth_use=random.randint(165900,185900)
        loss=totoal_in - auth_use   #44100
        charge_auth=random.randint(157500,165900)
        uncharge_auth=auth_use - charge_auth    #8400
        charge_measure=random.randint(141750,157500)
        charge_unmeasure=charge_auth - charge_measure   #15750
        uncharge_measure=random.randint(2400,uncharge_auth)
        uncharge_unmeasure=uncharge_auth - uncharge_measure #6000
        apparent_loss=random.randint(16280,loss)
        actual_loss=loss - apparent_loss    #27820
        unauth_use=random.randint(516,apparent_loss)
        statistic_error=apparent_loss - unauth_use  #15764
        money_back=charge_auth  #157500
        money_waste=loss + uncharge_auth    #52500

        wb = WBalance(name=name,totoal_in=totoal_in,auth_use=auth_use,loss=loss,charge_auth=charge_auth,uncharge_auth=uncharge_auth,charge_measure=charge_measure,charge_unmeasure=charge_unmeasure,uncharge_measure=uncharge_measure,uncharge_unmeasure=uncharge_unmeasure,apparent_loss=apparent_loss,actual_loss=actual_loss,unauth_use=unauth_use,statistic_error=statistic_error,money_back=money_back,money_waste=money_waste)

        db.session.add(wb)
    db.session.commit()


    


if __name__ == '__main__':
    manager.run()