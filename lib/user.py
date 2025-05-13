
class User:

    def __init__(self, user_id, email_address, password):
        assert isinstance(user_id, (int, None)), "bad type for 'id' - require optional 'int'"
        assert isinstance(email_address, str), "bad type for 'username' - require 'str'"
        assert isinstance(password, str), "bad type for 'password' - require 'str'"

        self.user_id = user_id
        self.email = email_address
        self.password = password
