from flask.views import MethodView
from flask import render_template, request, jsonify

class TopView(MethodView):
    def __init__(self, template):
        self.template = template

    def get(self):
        context = {}
        return render_template(self.template, **context)

    def post(self):
        if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            context = {}

            return jsonify({})
        return "Invalid request", 400
