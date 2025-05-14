# __created_by__ == Paul Patterson

class RegistrationValues:

    def __init__(self, email, password_1, password_2):
        self.email = email.strip()
        self.password_1 = password_1.strip()
        self.password_2 = password_2.strip()
        self.errors = []
        self.find_errors()

    def find_errors(self):
        if self.email_is_empty():
            self.errors.append('email cannot be empty')
        if not self.passwords_match():
            self.errors.append('passwords do not match')
        if self.password_is_empty():
            self.errors.append('password cannot be empty')

    def passwords_match(self):
        return self.password_1 == self.password_2

    def password_is_empty(self):
        return len(self.password_1) == 0

    def email_is_empty(self):
        return len(self.email) == 0

    def has_errors(self):
        return len(self.errors) > 0

    def first_error(self):
        assert len(self.errors) > 0
        return self.errors[0]

    @staticmethod
    def from_post_request(request):
        return RegistrationValues(request.form['email'], request.form['password_1'], request.form['password_2'])

    @staticmethod
    def all_empty():
        return RegistrationValues('', '', '')

