import json
import os

import pytest

from indeed.browser import Browser
from indeed.writer import write


@pytest.fixture(scope='session')
def browser() -> 'webdriver':
    """Создать браузер для test_scraper.py"""
    with Browser('./chromedriver/') as browser:
        yield browser


@pytest.fixture(scope='session')
def list_with_html_vacancies() -> list:
    """Список html-вакансий для test_parser.py"""
    with open("tests/test_data/data_for_parser.json", "r") as file:
        restored_list = json.load(file)
    return restored_list


@pytest.fixture(scope='session')
def prepare_data_and_create_table() -> list:
    """Список с готовыми списками вакансий пишутся в таблицу для проверки того что она создается."""
    with open('tests/test_data/data_for_writer.json', mode='r') as file:
        restored_list = json.load(file)

    write(restored_list)
    yield 'sheet.csv'

    os.remove('csv/sheet.csv')
