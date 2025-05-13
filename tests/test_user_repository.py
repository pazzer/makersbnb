# __created_by__ == Paul Patterson
import pytest

from lib.custom_exceptions import MalformedPasswordError, EmailAlreadyExistsError, MalformedEmailError, UnrecognisedIdError
from lib.user_repository import UserRepository

#### find_by_id

def test_find_by_id_throws_error_if_id_not_in_database(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    user_repository = UserRepository(db_connection)
    with pytest.raises(UnrecognisedIdError) as e:
        user_repository.find_by_id(99)
    error_message = str(e.value) 
    assert error_message == "id '99' not recognized."

def test_valid_find_by_id_returns_user_object(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    user_repository = UserRepository(db_connection)
    user = user_repository.find_by_id(3)
    assert user.email == 'carol@example.com'
    assert user.user_id == 3
    assert user.password == '24326224313224634b45356d65626b6a555971725762454d7056494a2e5457577231497a73344e6876617665303948324c5338685264323961656671'


#### find by email

def test_find_by_valid_email_returns_user_object(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    user_repository = UserRepository(db_connection)
    user = user_repository.find_by_email('carol@example.com')
    assert user.email == 'carol@example.com'
    assert user.user_id == 3
    assert user.password == '24326224313224634b45356d65626b6a555971725762454d7056494a2e5457577231497a73344e6876617665303948324c5338685264323961656671'

def test_find_by_email_returns_none_if_not_found(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    user_repository = UserRepository(db_connection)
    assert user_repository.find_by_email('carl@example.com') is None


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

#### Checking login credentials

def test_check_password_rejects_wrong_password(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    user_repository = UserRepository(db_connection)
    assert not user_repository.check_password('alice@example.com', 'password123')
    assert not user_repository.check_password('bob@example.com', '_@qwerty456')
    assert not user_repository.check_password('carol@example.com', 'securepass789$$')
    assert not user_repository.check_password('dave@example.com', '&&let&mei&n32')
    assert not user_repository.check_password('eve@example.com', 'a@dmi£n123')

def test_check_password_accepts_correct_password(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    user_repository = UserRepository(db_connection)
    assert user_repository.check_password('alice@example.com', 'password123!')
    assert user_repository.check_password('bob@example.com', '_@qwerty456£')
    assert user_repository.check_password('carol@example.com', 'securepass789$$^')
    assert user_repository.check_password('dave@example.com', '&&let&mei&n321')
    assert user_repository.check_password('eve@example.com', 'a@dmi£n1234')


