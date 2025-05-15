# __created_by__ == Paul Patterson
from operator import truediv

from lib.user import User
import bcrypt
from .custom_exceptions import EmailAlreadyExistsError, MalformedPasswordError, MalformedEmailError, UnrecognisedIdError


class UserRepository:

    def __init__(self, connection):
        self._connection = connection


    def find_by_email_and_password(self, email, plain_text_candidate):
        """Verifies that the password stored alongside `email`  matches
        `plain_text_candidate`."""
        rows = self._connection.execute("SELECT * FROM users WHERE email_address = %s", [email])
        if len(rows) == 0:
            return None
        else:
            assert len(rows) == 1, f"Error - found two records for '{email}'"
            stored_password = rows[0]['password']
            bytes_ = bytes.fromhex(stored_password)
            if bcrypt.checkpw(plain_text_candidate.encode('utf-8'), bytes_):
                return User.from_rowdict(rows[0])
            else:
                return None


    def find_by_id(self, id_):
        """Returns the `User` associated with `id_`. If no match is found an AssertionError
        is thrown."""
        rows = self._connection.execute("SELECT * FROM users WHERE user_id = %s", [id_])
        if len(rows) != 1:
            raise UnrecognisedIdError(f"id '{id_}' not recognized.")
        else:
            return User.from_rowdict(rows[0])


    def find_by_email(self, email):
        """Returns the `User` associated with `email`.
        - If no match is found `None` is returned.
        - If more than one match is found as AssertionError is thrown (v. troubling!)"""
        rows = self._connection.execute("SELECT * FROM users WHERE email_address = %s", [email])
        if len(rows) == 0:
            return None
        else:
            assert len(rows) == 1, f"Error - found two records for '{email}'"
            return User.from_rowdict(rows[0])


    def create_user(self, email, password):
        """Attempts to register a new user with the supplied credentials.
        - If `email` address already exists and EmailAlreadyExistsError is thrown.
        - For the password to be accepted it must be between 8 and 20 characters long AND contain
        at least one special character. If these conditions aren't met an MalformedPasswordError is thrown."""
        email = email.strip()
        password = password.strip()
        if self.find_by_email(email) is not None:
            raise EmailAlreadyExistsError(f"'{email}' already exists.")
        else:
            UserRepository._run_email_checks(email)
            UserRepository._run_password_checks(password)
            hashed_password = UserRepository._prepare_password_for_storage(password)
            self._connection.execute("INSERT INTO users (email_address, password, name) VALUES (%s, %s, %s)",
                                    [email, hashed_password, email])


    @staticmethod
    def _prepare_password_for_storage(password):
        """Passwords are converted to bytes, hashed, then stored as hex-strings in the database."""
        utf8_password = password.encode('utf-8')
        hashed = bcrypt.hashpw(utf8_password, bcrypt.gensalt())
        return hashed.hex()


    @staticmethod
    def _run_email_checks(email):
        """Emails can be registered if they meet the following criteria:
        - They are not already in use
        - They contain no spaces
        - They contain a '@' character
        - They end in '.com'
        - There is at least on character before the '@', and at least one after the '@' but before the '.com'.
        """
        if not email.endswith('.com'):
            raise MalformedEmailError('email should end with .com')
        elif len([ch for ch in email if ch == "@"]) != 1:
            raise MalformedEmailError('email must have a single "@" in it.')
        elif " " in email:
            raise MalformedEmailError('email must not contain whitespace')
        elif email.startswith('@'):
            raise MalformedEmailError('@ character cannot be first character')
        else:
            return None


    @staticmethod
    def _run_password_checks(password):
        """User passwords must:
        - be between 8 and 20 characters long
        - contain at least one of ! @ £ $ % ^ & '
        - contain no whitespace
        """
        if " " in password:
            raise MalformedPasswordError('password cannot contain whitespace')
        elif len(password) < 8:
            raise MalformedPasswordError('password must contain at least 8 characters.')
        elif len(password) > 20:
            raise MalformedPasswordError('password must be less than 20 characters or less.')
        elif len([ch for ch in password if ch in list("!@£$%^&")]) == 0:
            raise MalformedPasswordError('password must contain at least one of the following characters: ! @ £ $ % ^ & ')
        else:
            return

    def get_owner_of_space(self, space):
        rows = self._connection.execute('SELECT * FROM users WHERE user_id = %s', [space.user_id])
        assert len(rows) == 1, f"{space.name} doesn't appear to have an owner!"
        return User.from_rowdict(rows[0])
