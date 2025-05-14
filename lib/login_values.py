
class LoginValues:

    def __init__(self, email, password):
        self.email = email.strip()
        self.password = password.strip()
        self._errors = []
        self.find_errors()

    def find_errors(self):
        if self.email_is_empty():
            self._errors.append('email cannot be empty')
        if self.password_is_empty():
            self._errors.append('password cannot be empty')

    def has_errors(self):
        return len(self._errors) > 0

    def first_error(self):
        assert self.has_errors(), 'no errors found - check `has_errors() before calling this method.'
        return self._errors[0]

    def email_is_empty(self):
        return len(self.email) == 0

    def password_is_empty(self):
        return len(self.password) == 0

    @staticmethod
    def from_post_request(request):
        return LoginValues(request.form['email'], request.form['password'])

    @staticmethod
    def all_empty():
        return LoginValues('', '')
