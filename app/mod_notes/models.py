from app.mod_auth.models import User


class Note:
    def __init__(self, id: int = None, text: str = '', user_id: int = None, user: User = User()):
        self.id = id,
        self.text = text
        self.user_id = user_id
        self.user = user
