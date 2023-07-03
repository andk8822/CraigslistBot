import tempfile

from indeed.browser import Browser
from indeed.scraper import Scraper
from indeed.parser import Parser


class Run:
    """Поочередный запуск объектов Browser(), Scraper(), Parser()"""
    def __init__(self, vacancy: str, location: str, chromedriver_path: str) -> None:
        self._vacancy = vacancy
        self._location = location
        self._chromedriver_path = chromedriver_path

        browser = Browser(self._chromedriver_path).browser
        with tempfile.TemporaryFile(mode='a+', encoding='utf-8') as temp_html:
            Scraper(browser, self._vacancy, self._location, temp_html)
            temp_html.seek(0)
            Parser(self._vacancy, self._location, temp_html)
