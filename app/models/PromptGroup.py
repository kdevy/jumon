from app.bootstrap import db

class PromptGroup(db.Model):
    __tablename__ = "prompt_group"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), nullable=False)
    prompt = db.relationship("Prompt")
    updated = db.Column(db.DateTime, nullable=True)
