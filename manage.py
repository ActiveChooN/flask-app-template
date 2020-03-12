import os
from dotenv import load_dotenv

if os.path.exists(os.path.join(os.getcwd(), ".env")):
    load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"), verbose=True,
                override=False)

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='application/*')
    COV.start()

import sys
from flask_script import Manager
from application import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@manager.shell
def make_shell_context():
    return dict()


@manager.command
def test(coverage=False):
    """Run the unit tests."""

    import pytest
    pytest.main()


if __name__ == "__main__":
    manager.run()
