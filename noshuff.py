import os
from app import create_app, db
from app.models import User, Post, Comment
from flask_migrate import Migrate
import click
import re

app = create_app(os.getenv('FLASK_CONFIG'))
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Post=Post, Comment=Comment)
