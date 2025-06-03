from app.bootstrap import db

class Prompt(db.Model):
    __tablename__ = "prompt"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)