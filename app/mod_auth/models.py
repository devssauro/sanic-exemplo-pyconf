from passlib.hash import pbkdf2_sha512


class User:
    def __init__(self, id: int = None, email: str = '', password: str = '', name: str = ''):
        self.id = id
        self.email = email
        self.password = password
        self.name = name

    def to_dict(self):
        properties = ['id', 'email', 'password', 'name']
        return {prop: getattr(self, prop, None) for prop in properties}
