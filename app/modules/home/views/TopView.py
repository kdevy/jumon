from collections import defaultdict
from flask.views import MethodView
from flask import render_template, request, jsonify, current_app
from sqlalchemy import desc, asc
from app.models import Prompt, PromptGroup
from app.bootstrap import db

class TopView(MethodView):
    def __init__(self, template):
        self.template = template

    def search(self):
        query = db.session.query(
            PromptGroup.id,
            PromptGroup.name,
            PromptGroup.updated,
        ) \
        .order_by(desc(PromptGroup.updated), desc(PromptGroup.id))
        prompt_group_list = db.session.execute(query).mappings().all()

        query = db.session.query(
            Prompt.id,
            Prompt.prompt_group_id,
            Prompt.name,
            Prompt.type,
            Prompt.is_favorite,
            Prompt.updated,
        ) \
        .order_by(asc(Prompt.type), desc(Prompt.updated), desc(Prompt.id))
        prompt_list = db.session.execute(query).mappings().all()

        return [prompt_group_list, prompt_list]

    def merge_prompt_group_list(self, prompt_group_list, prompt_list):
        grouped_prompts = defaultdict(list)
        for prompt in prompt_list:
            grouped_prompts[prompt['prompt_group_id']].append(prompt)

        result = []
        for group in prompt_group_list:
            dict_group = dict(group)
            dict_group['prompt'] = grouped_prompts.get(group['id'], [])
            result.append(dict_group)

        return result

    def get(self):
        prompt_group_list = self.merge_prompt_group_list(*self.search())
        context = {
            "prompt_group_list": prompt_group_list,
        }
        current_app.logger.debug(prompt_group_list)
        return render_template(self.template, **context)

    def post(self):
        if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            mode = request.form.get('mode')
            if mode == "fetch_prompt_contents":
                id = request.form.get('id')
                if not id:
                    return jsonify({"errors": "require param 'id'"})

                query = db.session.query(Prompt).filter(Prompt.id == id)
                prompt = db.session.execute(query).first()

                if prompt[0].type == 2:
                    query = db.session.query(Prompt) \
                    .filter(Prompt.prompt_group_id == prompt[0].prompt_group_id) \
                    .filter(Prompt.type == 1)
                    base_prompt = db.session.execute(query).first()
                    return jsonify({"base_prompt": base_prompt[0].to_dict(), "derivation_prompt": prompt[0].to_dict()})

                return jsonify({"base_prompt": prompt[0].to_dict()})
            else:
                return jsonify({"errors": "invalid param 'mode'"})
        return "Invalid request", 400
