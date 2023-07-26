import pytest


from indeed import scraper


def test_go_to_site(test_browser):
    scraper.go_to_site(test_browser)
    assert test_browser.current_url == 'https://ca.indeed.com/', 'Текущий адрес не соответствует https://ca.indeed.com/'
