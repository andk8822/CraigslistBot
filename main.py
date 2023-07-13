import click

from indeed.browser import Browser
from indeed.scraper import *
from indeed.parser import Vacancy
from indeed.writer import write


@click.command()
@click.option('--vacancy_name', default='Barber', prompt='Введите вакансию:', help='Поиск вакансии', type=str)
@click.option('--location_name', default='Calgary', prompt='Введите локацию:', help='Поиск локации', type=str)
@click.option('--chromedriver_path', default='./chromedriver/', help='Папка с chromedriver', type=str)
def run_indeed(vacancy_name: str, location_name: str, chromedriver_path: str) -> None:
    with Browser(chromedriver_path) as browser:
        go_to_site(browser)
        input_search_parameters(browser, vacancy_name, location_name)
        if search_result(browser):
            vacancies = Vacancy()
            scrape(browser, vacancies)
            vacancies_list = vacancies.get_vacancies
            write(vacancies_list, vacancy_name, location_name)


if __name__ == "__main__":
    run_indeed()
