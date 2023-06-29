import tempfile

from indeed.browser import Browser
from indeed.scraper import Scraper
from indeed.parser import Parser


class Run:
    """Поочередный запуск объектов Browser(), Scraper(), Parser()"""
    def __init__(self, what: str, where: str, chromedriver_path: str) -> None:
        self._what = what
        self._where = where
        self._chromedriver_path = chromedriver_path

        browser = Browser(self._chromedriver_path).browser
        with tempfile.TemporaryFile(mode='a+', encoding='utf-8') as temp_html:
            Scraper(browser, self._what, self._where, temp_html)
            temp_html.seek(0)
            Parser(self._what, self._where, temp_html)
