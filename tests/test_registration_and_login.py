
from playwright.sync_api import Page, expect

# Helpers

def fill(field, value, page):
    page.fill(f"input[name={field}]", value)

def click(field, page):
    page.click(f'text={field}')

def go_home(page, test_web_address):
    page.goto(f"http://{test_web_address}/makersbnb.com")

def go_to(relroute, page, test_web_address):
    relroute = relroute.strip()
    if relroute == "":
        go_home(page, test_web_address)
    else:
        page.goto(f"http://{test_web_address}/makersbnb.com/{relroute}")

def seed_db(db_connection):
    db_connection.seed("seeds/makersbnb.sql")

def make_url(relurl, test_web_address):
    relurl = relurl.strip()
    if relurl == '':
        return f'http://{test_web_address}/makersbnb.com'
    else:
        return f'http://{test_web_address}/makersbnb.com/{relurl}'

def locate(tag, page):
    return page.locator(tag)


## Tests

def test_can_access_login_via_link_on_registration_page(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb.sql")
    page.goto(f"http://{test_web_address}/makersbnb.com")

    page.click('text=login')
    expect(page).to_have_url(f'http://{test_web_address}/makersbnb.com/login')

# Login

def test_bad_email_at_login_raises_warning(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb.sql")
    page.goto(f"http://{test_web_address}/makersbnb.com/login")

    page.fill("input[name='email']", "lice@example.com")
    page.fill("input[name='password']", "password123!")
    page.click("text=Submit")

    errors = page.locator(".t-errors")
    expect(errors).to_have_text("⛔ email and/or password not recognised. Try Again.")

def test_bad_password_at_login_raises_warning(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb.sql")
    page.goto(f"http://{test_web_address}/makersbnb.com/login")

    page.fill("input[name='email']", "lice@example.com")
    page.fill("input[name='password']", "password123")
    page.click("text=Submit")

    errors = page.locator(".t-errors")
    expect(errors).to_have_text("⛔ email and/or password not recognised. Try Again.")

def test_successful_login(db_connection, page, test_web_address):
    seed_db(db_connection)
    go_to('login', page, test_web_address)

    fill('email', "alice@example.com", page)
    fill('password', "password123!", page)

    click('Submit', page)

    expect(page).to_have_url(make_url('spaces', test_web_address))
    email_el = locate('.t-user-email', page)
    expect(email_el).to_contain_text('alice@example.com')

def test_can_log_out():
    raise NotImplementedError("test placeholder")

# Register

def test_can_register_with_valid_email_and_password():
    raise NotImplementedError("test placeholder")

def test_cannot_register_with_duplicate_email():
    raise NotImplementedError("test placeholder")

def test_cannot_register_with_bad_email():
    raise NotImplementedError("test placeholder")

def test_cannot_register_with_bad_password():
    raise NotImplementedError("test placeholder")



