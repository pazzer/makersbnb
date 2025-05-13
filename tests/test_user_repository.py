# __created_by__ == Paul Patterson
import pytest

from lib.custom_exceptions import MalformedPasswordError, EmailAlreadyExistsError, MalformedEmailError
from lib.user_repository import UserRepository

#### Registering an email

def test_cannot_register_existing_email_address(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    user_repository = UserRepository(db_connection)
    with pytest.raises(EmailAlreadyExistsError) as e:
        user_repository.register_new_user('alice@example.com', '12345678!')
    error_message = str(e.value)
    assert error_message == f"'alice@example.com' already exists."

def test_cannot_register_email_with_no_dotcom_at_end(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    user_repository = UserRepository(db_connection)
    with pytest.raises(MalformedEmailError) as e:
        user_repository.register_new_user('alice@example.con', '12345678!')
    error_message = str(e.value)
    assert error_message == 'email should end with .com'

def test_cannot_register_email_with_no_curly_at_character(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    user_repository = UserRepository(db_connection)
    with pytest.raises(MalformedEmailError) as e:
        user_repository.register_new_user('alice_example.com', '12345678!')
    error_message = str(e.value)
    assert error_message == 'email must have a single "@" in it.'

def test_cannot_register_email_that_contains_whitespace(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    user_repository = UserRepository(db_connection)
    with pytest.raises(MalformedEmailError) as e:
        user_repository.register_new_user('alice@example .com', '12345678!')
    error_message = str(e.value)
    assert error_message == 'email must not contain whitespace'

def test_cannot_register_email_that_starts_with_curly_at_character(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    user_repository = UserRepository(db_connection)
    with pytest.raises(MalformedEmailError) as e:
        user_repository.register_new_user('@example.com', '12345678!')
    error_message = str(e.value)
    assert error_message == '@ character cannot be first character'

def test_can_register_valid_email_address(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    user_repository = UserRepository(db_connection)
    retval = user_repository.register_new_user('rupert@example.com', '12345678!')
    assert retval is None

#### Registering a password


def test_cannot_register_password_containing_whitespace(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    user_repository = UserRepository(db_connection)
    with pytest.raises(MalformedPasswordError) as e:
        _ = user_repository.register_new_user('gottfried@go_mail.com', 'a23 456789!')
    error_message = str(e.value)
    assert error_message == 'password cannot contain whitespace'

def test_cannot_register_password_without_special_character(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    user_repository = UserRepository(db_connection)
    with pytest.raises(MalformedPasswordError) as e:
        _ = user_repository.register_new_user('gottfried@go_mail.com', 'a23456789')
    error_message = str(e.value)
    assert error_message == 'password must contain at least one of the following characters: ! @ £ $ % ^ & '


def test_cannot_register_password_with_more_than_20_characters(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    user_repository = UserRepository(db_connection)
    with pytest.raises(MalformedPasswordError) as e:
        _ = user_repository.register_new_user('gottfried@go_mail.com', '12345678!a12345678!a12345678!a')
    error_message = str(e.value)
    assert error_message == 'password must be less than 20 characters or less.'


def test_cannot_register_password_less_than_8_characters(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    user_repository = UserRepository(db_connection)
    with pytest.raises(MalformedPasswordError) as e:
        _ = user_repository.register_new_user('gottfried@go_mail.com', 'a23456!')
    error_message = str(e.value)
    assert error_message == 'password must contain at least 8 characters.'

def test_can_register_valid_password(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    user_repository = UserRepository(db_connection)
    assert user_repository.register_new_user('gottfried@go_mail.com', '12345678!') is None


# def test_can_register_valid_password(db_connection):
#     db_connection.seed("seeds/makersbnb.sql")
#     user_repository = UserRepository(db_connection)
#     assert user_repository.check_password('puss@notmail.com', 'over_the_🌝')
#     assert user_repository.check_password('fred_frost_02@gmail.com', '12345678!')
#     assert user_repository.check_password('user1@hotmail.com', 'I 💜 🚗 and 🚜')

#

#
# def test_register_password_too_short(db_connection):

#
# def test_register_password_lacks_special_character(db_connection):

#
#
# def test_find_by_id_invalid(db_connection):
#     db_connection.seed("seeds/login_form.sql")
#     user_repository = UserRepository(db_connection)
#     with pytest.raises(AssertionError) as e:
#         user = user_repository.find_by_id(0)
#     assert str(e.value) == f"id '0' not recognized."
