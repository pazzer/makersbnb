
from playwright.sync_api import Page, expect

def test_can_access_login_via_link_on_registration_page(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb.sql")
    page.goto(f"http://{test_web_address}/makersbnb.com")

    page.click('text=login')
    expect(page).to_have_url(f'http://{test_web_address}/makersbnb.com/login')

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
    db_connection.seed("seeds/makersbnb.sql")
    page.goto(f"http://{test_web_address}/makersbnb.com/login")

    page.fill("input[name='email']", "alice@example.com")
    page.fill("input[name='password']", "password123!")


    page.click("text=Submit")
    # TODO: complete once fully understand sessions


