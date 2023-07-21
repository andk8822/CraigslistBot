import click

from indeed.browser import Browser
from indeed import scraper
from indeed.parser import Vacancy
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
            vacancies = Vacancy()  # Объект класса "Вакансия".
            scraper.scrape(browser, vacancies)  # Передача html-блоков вакансий и их обработка.
            vacancies_list = vacancies.get_vacancies  # Получение обработанного списка вакансий.
            write(vacancies_list, vacancy_name, location_name)  # Запись списка вакансий в csv-файл.
        else:  # Если нет поисковых результатов.
            pass


if __name__ == "__main__":
    run_indeed()
