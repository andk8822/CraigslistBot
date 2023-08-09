import json
import os
from typing import List

import pytest
from selenium import webdriver

from indeed.browser import Browser
from indeed.parser import parse_html_vacancy, Vacancy
from indeed.csv_writer import write


@pytest.fixture(scope='session')
def browser() -> webdriver:
    """Создать браузер для test_scraper.py"""
    with Browser('./chromedriver/') as browser:
        yield browser


@pytest.fixture(scope='session')
def vacancies_html() -> list:
    """Список html-вакансий для test_parser.py"""
    with open("tests/test_data/data_for_parser_n_writer.json", "r") as file:
        restored_list = json.load(file)
    return restored_list


@pytest.fixture(scope='session')
def prepare_data_and_create_table() -> list:
    """Список с готовыми списками вакансий пишутся в таблицу для проверки того что она создается."""
    vacancies_ready: List[Vacancy] = list()

    with open('tests/test_data/data_for_parser_n_writer.json', mode='r') as file:
        restored_list = json.load(file)

    for vacancy_html in restored_list:
        vacancies_ready.append(parse_html_vacancy(vacancy_html))

    write(vacancies_ready)
    yield 'sheet.csv'

    os.remove('csv/sheet.csv')
