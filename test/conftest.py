import pytest

from indeed.browser import Browser


@pytest.fixture(scope='session')
def test_browser():
    with Browser('./chromedriver/') as browser:
        yield browser
