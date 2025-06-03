
"""
python -m bin.create_all
"""
from app.bootstrap import create_app

app = create_app()

from app.bootstrap import db
from app.models import Prompt, PromptGroup

with app.app_context():
    db.create_all()