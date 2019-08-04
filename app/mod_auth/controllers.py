from typing import List

from sanic import Blueprint, response
from sanic_jwt import protected
from app.mod_auth.models import User

users: List[User] = []
auth_blueprint = Blueprint('auth_blueprint', url_prefix='/user')


@auth_blueprint.route('/register', methods=['POST'])
async def register_post(request):

    if len(list(filter(lambda u: u.email == request.json['email'], users))) == 0:
        user = User(**request.json)
        user.id = len(users) + 1
        users.append(user)

        return response.json({
            'id': user.id,
            'msg': 'Usuário criado!'
        }, status=201)
    else:
        return response.json({
            'msg': 'Usuário com este e-mail já existe no sistema.'
        }, status=401)


@auth_blueprint.route('', methods=['GET'])
@protected()
async def user_get(request):
    if len(users) > 0:
        return response.json({
            'users': list(map(lambda u: {
                'id': u.id,
                'name': u.name,
                'email': u.email
            }, users))
        })
    else:
        return response.json({
            'msg': 'Não já usuários cadastrados'
        })
