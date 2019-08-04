from sanic import Sanic
from sanic.response import json
from app.mod_notes.controllers import notes_blueprint
from app.mod_auth.controllers import auth_blueprint
from sanic_jwt import exceptions, initialize
from app.mod_auth.controllers import users
from passlib.hash import pbkdf2_sha512
app = Sanic()
app.blueprint(auth_blueprint)
app.blueprint(notes_blueprint)


async def authenticate(request):
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email or not password:
        raise exceptions.AuthenticationFailed("Informe o email e a senha")

    user = None
    if len(users) > 0:
        user = list(filter(lambda u: u.email == email, users))[0]
    if user is None:
        raise exceptions.AuthenticationFailed("Usuário não encontrado.")

    if password != user.password:
        raise exceptions.AuthenticationFailed("Senha incorreta.")

    return {'user_id': user.id}


async def retrieve_user(request, payload, *args, **kwargs):
    if payload:
        user_id = payload.get('user_id', None)
        print(payload)
        user = None
        if len(users) > 0:
            _user = list(filter(lambda u: u.id == user_id, users))
            if len(_user) > 0:
                user = _user[0]

        return user
    else:
        return None

initialize(app, authenticate=authenticate, retrieve_user=retrieve_user)


@app.route("/")
async def test(request):
    return json({"hello": app.blueprints})

