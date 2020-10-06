import os
from app import create_app, db
from app.models import User, Post
from flask_migrate import Migrate
import click
import re

app = create_app(os.getenv('FLASK_CONFIG'))
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Post=Post)

@app.cli.command()
@click.argument("target", required=False)
def test(target=None):
    import unittest
    if target:
        module_search = re.compile(r"[.]\w+$").search(target)
        if module_search:
            module_name = target[:module_search.start()]
            file_name = target[(module_search.start() + 1):module_search.end()]
            tests = unittest.TestLoader().discover(f'tests.{module_name}', f'{file_name}*')
        else:
            tests = unittest.TestLoader().discover('tests', f'{target}*')
    else:
        tests = unittest.TestLoader().discover('tests')

    unittest.TextTestRunner(verbosity=2).run(tests)
