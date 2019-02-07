from flask import Blueprint, jsonify
from poc.todo import model as todo
from werkzeug.exceptions import NotFound


CT_JSON = {'ContentType': 'application/json'}


bp = Blueprint('todo', __name__)


#
# Base route
#
@bp.route('/', methods=['GET'])
def get_all_todos():
    rows = todo.get_all()

    if not rows:
        return jsonify({'todos': []}), 200, CT_JSON

    keys = rows[0].keys()
    items = [dict(zip(keys, tuple(row))) for row in rows]
    return jsonify({'todos': items}), 200, CT_JSON


@bp.route('/', methods=['POST'])
def create_todo():
    # TODO
    return jsonify({'error': 'not_implemented'}), 400, CT_JSON


#
# Operations on one element.
#
@bp.route('/<int:id>', methods=['GET'])
def get_one_by_id(id):
    row = todo.get_by_id(id)

    if not row:
        raise NotFound()

    return jsonify({'todo': dict(row)}), 200, CT_JSON


@bp.route('/<int:id>', methods=['POST'])
def edit_todo():
    # TODO
    return jsonify({'error': 'not_implemented'}), 400, CT_JSON
