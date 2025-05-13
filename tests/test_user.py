from lib.user import User

def test_create_user():
    user = User(1, "billy_bobby@hotmail.com", "12345")
    assert user.user_id == 1
    assert user.email_address == "billy_bobby@hotmail.com"
    assert user.password == "12345"
