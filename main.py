import click

from indeed.browser import Browser
from indeed.scraper import *


@click.command()
@click.option('--vacancy', default='Barber', prompt='Введите вакансию', help='Поиск вакансии')
@click.option('--location', default='Calgary', prompt='Введите локацию', help='Поиск локации')
@click.option('--chromedriver_path', default='./chromedriver/', help='Папка с chromedriver')
def run_indeed(vacancy: str, location: str, chromedriver_path: str) -> None:
    """Создать csv-таблицу вакансий с сайта ca.indeed.com по заданным параметрам поиска"""
    with Browser(chromedriver_path) as browser:
        go_to_site(browser)
        input_search_parameters(browser, vacancy, location)
        if search_result(browser):
            scrape(browser)

        """
            Если нет объектов, в классе нет смысла. Выдержать SRP. Выдержать тесты.

            with browser as browser:
                go_to_site(browser)
                input_search_params(browser, vacancy, location)
                if search_result(browser):
                    vacancies = Vacancy(vacancy, location)
                    scrape(browser, vacancies)
                    vacancies.get_csv()

                class Vacancy:
                    def __init__()
                    def _parse()  # Тестируется при передаче html-блоков
                    def _amount()
                    def add_vacancy_html()
                    def get_csv()
            """


if __name__ == "__main__":
    run_indeed()
