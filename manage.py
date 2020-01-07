import os
from basedir import basedir
from dotenv import load_dotenv

if os.path.exists(os.path.join(basedir, ".env")):
    load_dotenv(dotenv_path=os.path.join(basedir, ".env"), verbose=True,
                override=False)

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='application/*')
    COV.start()

import sys
from flask_script import Manager
from flask_migrate import Migrate, upgrade, MigrateCommand
from application import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(db=db)


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def deploy():
    """Makes deployment task. Upgrades database tables, creates the db
       tables, roles and admin."""
    upgrade()


@manager.command
def destroy_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        cov_dir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=cov_dir)
        print('HTML version: file://{}/index.html'.format(cov_dir))
        COV.erase()


if __name__ == "__main__":
    manager.run()
