import pytest

from indeed.browser import Browser


@pytest.fixture(scope='session')
def test_browser():
    browser = Browser('./chromedriver/').browser
    yield browser
    browser.quit()
