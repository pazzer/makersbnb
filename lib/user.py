
class User:

    def __init__(self, user_id, email_address, password, name):
        assert isinstance(user_id, (int, None)), "bad type for 'id' - require optional 'int'"
        assert isinstance(email_address, str), "bad type for 'username' - require 'str'"
        assert isinstance(password, str), "bad type for 'password' - require 'str'"
        assert isinstance(name, str), "bad type for 'password' - require 'str'"

        self.user_id = user_id
        self.email_address = email_address
        self.password = password
        self.name = name


    @staticmethod
    def from_rowdict(rowdict):
        return User(rowdict['user_id'], rowdict['email_address'], rowdict['password'], rowdict['name'])
