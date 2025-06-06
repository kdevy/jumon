from app.bootstrap import db

class Prompt(db.Model):
    __tablename__ = "prompt"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prompt_group_id = db.Column(db.ForeignKey('prompt_group.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    type = db.Column(db.SmallInteger, nullable=False, server_default="1")
    name = db.Column(db.String(300), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    is_favorite = db.Column(db.SmallInteger, nullable=True, server_default="0")
    updated = db.Column(db.DateTime, nullable=True)