
from types import NoneType

import flask_login


class User(flask_login.UserMixin):

    def __init__(self, user_id, email_address, password, name=None):
        assert isinstance(user_id, (int, None)), "bad type for 'id' - require optional 'int'"
        assert isinstance(email_address, str), "bad type for 'username' - require 'str'"
        assert isinstance(password, str), "bad type for 'password' - require 'str'"
        assert isinstance(name, (str, NoneType)), "bad type for 'name' - require 'str'"

        self.user_id = user_id
        self.email_address = email_address
        self.password = password
        self.name = name if name is not None else email_address


    @staticmethod
    def from_rowdict(rowdict):
        return User(rowdict['user_id'], rowdict['email_address'], rowdict['password'], rowdict['name'])


    def get_id(self):
        return str(self.user_id)






