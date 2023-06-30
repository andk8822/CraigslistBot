import pytest


def test_browser(browser):
    assert browser is not None, 'Browser has not been created!'
