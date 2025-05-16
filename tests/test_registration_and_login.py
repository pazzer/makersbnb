

from playwright.sync_api import Page, expect

# Helpers

def fill(field, value, page):
    page.fill(f"input[name={field}]", value)

def click(field, page):
    page.click(f'text={field}')

def go_home(page, test_web_address):
    page.goto(f"http://{test_web_address}/")

def go_to(relroute, page, test_web_address):
    relroute = relroute.strip()
    if relroute == "":
        go_home(page, test_web_address)
    else:
        page.goto(f"http://{test_web_address}/{relroute}")

def seed_db(db_connection):
    db_connection.seed("seeds/makersbnb.sql")

def make_url(relurl, test_web_address):
    relurl = relurl.strip()
    if relurl == '':
        return f'http://{test_web_address}'
    else:
        return f'http://{test_web_address}/{relurl}'

def locate(tag, page):
    return page.locator(tag)

def get_input_field(field_name, page):
    return page.locator(f'input[name={field_name}]')


## Tests

def test_can_access_login_via_link_on_registration_page(db_connection, page, test_web_address):
    seed_db(db_connection)
    go_home(page, test_web_address)
    expect(page).to_have_url(make_url('register', test_web_address))

    click('login', page)
    login_url = make_url('login', test_web_address)
    expect(page).to_have_url(login_url)

# Login

def test_bad_email_at_login_raises_warning(db_connection, page, test_web_address):
    seed_db(db_connection)
    go_to('login', page, test_web_address)

    fill('email', 'lice@example.com', page)
    fill('password', 'password123!', page)
    click('Submit', page)

    error_el = locate('.t-errors', page)
    expect(error_el).to_have_text("⛔ email and/or password not recognised. Try Again.")


def test_successful_login(db_connection, page, test_web_address):
    seed_db(db_connection)
    go_to('login', page, test_web_address)

    fill('email', "alice@example.com", page)
    fill('password', "password123!", page)

    click('Submit', page)

    spaces_url = make_url('spaces', test_web_address)
    expect(page).to_have_url(spaces_url)
    email_el = locate('.t-user-name', page)
    expect(email_el).to_contain_text('Alice')

def test_can_log_out(db_connection, page, test_web_address):
    seed_db(db_connection)
    go_to('login', page, test_web_address)

    fill('email', "alice@example.com", page)
    fill('password', "password123!", page)

    click('Submit', page)

    spaces_url = make_url('spaces', test_web_address)
    expect(page).to_have_url(spaces_url)

    click('Log Out', page)

    # Redirected to login page
    login_url = make_url('login', test_web_address)
    expect(page).to_have_url(login_url)

    # no more access to spaces
    go_to('spaces', page, test_web_address)
    assert page.url.split('/')[-1].startswith('login?next')

    # Nothing in input field
    field = get_input_field('email', page)
    expect(field).to_have_value("")

    field = get_input_field('password', page)
    expect(field).to_have_value("")

# Register

def test_can_register_with_valid_email_and_password(db_connection, page, test_web_address):
    seed_db(db_connection)
    go_to('register', page, test_web_address)

    fill('email', "carl@example.com", page)
    fill('password_1', "password1234!", page)
    fill('password_2', "password1234!", page)
    click('Create my Account', page)

    h1 = locate('h1', page)
    expect(h1).to_have_text('✅ Registration complete!')

    click('log in', page)
    fill('email', "carl@example.com", page)
    fill('password', "password1234!", page)
    click('Submit', page)

    username_el = locate('.t-user-name', page)
    expect(username_el).to_have_text('carl@example.com')


def test_cannot_register_with_duplicate_email(db_connection, page, test_web_address):
    seed_db(db_connection)
    go_to('register', page, test_web_address)

    fill('email', "carol@example.com", page)
    fill('password_1', "password12345!", page)
    fill('password_2', "password12345!", page)
    click('Create my Account', page)

    errors_el = locate('.t-errors', page)
    expect(errors_el).to_have_text(" ⚠️ 'carol@example.com' already exists.")




# #
# # def test_cannot_register_with_bad_email():
# #     raise NotImplementedError("test placeholder")
# #
# # def test_cannot_register_with_bad_password():
# #     raise NotImplementedError("test placeholder")
#
#
#
