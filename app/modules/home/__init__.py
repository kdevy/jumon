import os
from flask import Blueprint
from .views.TopView import TopView

app = Blueprint(os.path.basename(os.path.dirname(__file__)), __name__, template_folder="templates", static_folder="static")
app.add_url_rule("/", view_func=TopView.as_view("top", "top.html"))