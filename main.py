from typing import List

import click

from indeed.browser import Browser
from indeed import scraper
from indeed.parser import Vacancy, parse_html_vacancy
from indeed.csv_writer import write


@click.command()
@click.option('--vacancy_name', default='Barber', prompt='Введите вакансию:', help='Поиск вакансии', type=str)
@click.option('--location_name', default='Calgary', prompt='Введите локацию:', help='Поиск локации', type=str)
@click.option('--chromedriver_path', default='./chromedriver/', help='Папка с chromedriver', type=str)
def run_indeed(vacancy_name: str, location_name: str, chromedriver_path: str) -> None:
    with Browser(chromedriver_path) as browser:
        scraper.go_to_site(browser)  # Перейти на ca.indeed.com.
        scraper.input_search_parameters(browser, vacancy_name, location_name)  # Ввести поисковые запросы.
        if scraper.check_result(browser):  # Если есть вакансии.
            vacancies_html: List[str] = scraper.Scraper(browser).get_vacancies  # Список html-вакансий.
            vacancies_ready: List[Vacancy] = list()

            # Список распарсеных html-вакансий.
            for vacancy_html in vacancies_html:
                vacancies_ready.append(parse_html_vacancy(vacancy_html))

            # Запрос имени таблицы от пользователя
            sheet_name = click.prompt('Введите имя для таблицы, или нажмите "Enter"', default='')

            # Записать список списков в таблицу.
            write(vacancies_ready, vacancy_name, location_name, sheet_name)
        else:  # Если нет поисковых результатов.
            pass


if __name__ == "__main__":
    run_indeed()
