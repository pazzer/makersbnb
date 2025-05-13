
class User:

    def __init__(self, id_, email, password):
        assert isinstance(id_, (int, None)), "bad type for 'id' - require optional 'int'"
        assert isinstance(email, str), "bad type for 'username' - require 'str'"
        assert isinstance(password, str), "bad type for 'password' - require 'str'"

        self.id = id_
        self.email = email
        self.password = password
