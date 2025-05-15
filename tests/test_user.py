from lib.user import User

def test_user_constructor():
    user = User(1, "billy_bobby@hotmail.com", "12345", 'Billy')
    assert user.user_id == 1
    assert user.email_address == "billy_bobby@hotmail.com"
    assert user.password == "12345"
    assert user.name == 'Billy'

def test_create_user_from_rowdict(db_connection):
    db_connection.seed("seeds/makersbnb.sql")
    rows = db_connection.execute("SELECT * FROM users WHERE user_id = 6")
    assert len(rows) == 1
    user = User.from_rowdict(rows[0])
    assert user.user_id == 6
    assert user.email_address == 'developer@example.com'
    assert user.password == "24326224313224736c3978776b566563534e4d69377057625771757865474a70386b3063413579634c666d5763706261514b7a444450504b50656343"
    assert user.name == 'Developer'

