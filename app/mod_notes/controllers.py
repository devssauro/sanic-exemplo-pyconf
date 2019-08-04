from sanic import Blueprint
from sanic_jwt import protected, inject_user
from sanic.response import json
from app.mod_notes.models import Note
from app.mod_auth.controllers import users
from typing import List


notes: List[Note] = []
notes_blueprint = Blueprint('notes_blueprint', url_prefix='/note')


@notes_blueprint.route('/all', methods=['GET'])
async def all_notes_get(request):
    return json({
        'notes': list(map(lambda n: {
            'id': n.id,
            'text': n.text,
            'user': {
                'id': list(filter(lambda u: u.id == n.user_id, users))[0].id,
                'email': list(filter(lambda u: u.id == n.user_id, users))[0].email,
                'name': list(filter(lambda u: u.id == n.user_id, users))[0].name,
            }
        }, notes))
    })


@notes_blueprint.route('', methods=['POST'])
@protected()
@inject_user()
async def notes_post(request, user):
    j_data = dict(request.json)
    j_data['user_id'] = user.id
    note = Note(**j_data)
    note.id = len(notes) + 1
    notes.append(note)
    return json({
        'id': note.id,
        'msg': 'Nota Criada',
        'text': note.text
    }, status=201)


@notes_blueprint.route('', methods=['GET'])
@protected()
@inject_user()
async def notes_get(request, user):
    return json({
        'notes': list(map(lambda n: {
            'id': n.id,
            'text': n.text
        }, list(filter(lambda n: n.user_id == user.id, notes))))
    })


@notes_blueprint.route('/<_id:int>', methods=['GET'])
@protected()
@inject_user()
async def notes_get_id(request, user, _id):
    _note: List[Note] = list(filter(lambda n: n.user_id == user.id and n.id == _id, notes))
    if len(_note) > 0:
        return json({
            'id': _note[0].id,
            'text': _note[0].text
        }, status=200)
    else:
        return json({
            'msg': 'Nota não encontrada'
        }, status=404)


@notes_blueprint.route('/<_id:int>', methods=['PUT'])
@protected()
@inject_user()
async def notes_put_id(request, user, _id):
    _note: List[Note] = list(filter(lambda n: n.user_id == user.id and n.id == _id, notes))
    if len(_note) > 0:
        _note[0].text = request.json['text']
        for note in notes:
            if note.id == _id:
                note = _note[0]
        return json({
            'id': _note[0].id,
            'text': _note[0].text,
            'msg': 'Nota alterada'
        }, status=200)
    else:
        return json({
            'msg': 'Nota não encontrada'
        }, status=404)


@notes_blueprint.route('/<_id:int>', methods=['DELETE'])
@protected()
@inject_user()
async def notes_delete_id(request, user, _id):
    _note: List[Note] = list(filter(lambda n: n.user_id == user.id and n.id == _id, notes))

    if len(_note) > 0:
        notes.remove(_note[0])

        return json({
            'id': _note[0].id,
            'text': _note[0].text,
            'msg': 'Nota excluída'
        }, status=200)
    else:
        return json({
            'msg': 'Nota não encontrada'
        }, status=404)
