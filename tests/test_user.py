from lib.user import User

def test_create_user():
    user = User(1, "billy_bobby@hotmail.com", "12345")
    assert user.id == 1
    assert user.email == "billy_bobby@hotmail.com"
    assert user.password == "12345"
