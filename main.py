import click

from indeed.browser import Browser
from indeed import scraper
from indeed.parser import ParserVacancy
from indeed.writer import write


@click.command()
@click.option('--vacancy_name', default='Barber', prompt='Введите вакансию:', help='Поиск вакансии', type=str)
@click.option('--location_name', default='Calgary', prompt='Введите локацию:', help='Поиск локации', type=str)
@click.option('--chromedriver_path', default='./chromedriver/', help='Папка с chromedriver', type=str)
def run_indeed(vacancy_name: str, location_name: str, chromedriver_path: str) -> None:
    with Browser(chromedriver_path) as browser:
        scraper.go_to_site(browser)  # Перейти на ca.indeed.com.
        scraper.input_search_parameters(browser, vacancy_name, location_name)  # Ввести поисковые запросы.
        if scraper.search_result(browser):  # Если есть вакансии.
            vacancies_list_with_htmls = scraper.Scraper(browser).get_vacancies  # Список с html из объекта Scraper.
            vacancies_parser_object = ParserVacancy()  # Объект Parser.

            # Передать html элементы списка в объект Parser для парсинга.
            for vacancy_html in vacancies_list_with_htmls:
                vacancies_parser_object.save_vacancy(vacancy_html)

            vacancies_list_with_lists = vacancies_parser_object.get_vacancies  # Список списков объекта Parser.
            write(vacancies_list_with_lists, vacancy_name, location_name)  # Записать список списков в таблицу.
        else:  # Если нет поисковых результатов.
            pass


if __name__ == "__main__":
    run_indeed()
