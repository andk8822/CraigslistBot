import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from indeed.logger_settings import logger


# def page_not_found_error(browser: webdriver):
#     """Сценарий для страницы-404"""
#     try:
#         for i in range(1, 3):  # Сделать 2 попытки перезагрузки страницы.
#             browser.find_element(By.CSS_SELECTOR, 'section.error-content')
#             logger.info(f'Страница 404. Попытка перезагрузки #{i} из 3...')
#             browser.refresh()
#             time.sleep(1)
#     except NoSuchElementException:  # 404 больше нет.
#         return False
#     else:  # 404 на месте.
#         logger.info('Перезагрузка страницы не дает результата, возможно проблемы с интернетом')
#         logger.debug('Проблемы с работе scraper.page_not_found_error')
#         return True

def page_refresh_decorator(func):
    """Декоратор для перезагрузки страницы и повторный запуск внутренней функции."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoSuchElementException:
            logger.info('Попытка перезагрузки с помощью page_refresh_decorator..')
            browser.refresh()
            return func(*args, **kwargs)
    return wrapper


def go_to_site(browser: webdriver) -> None:
    """Перейти на сайт"""
    browser.get('https://ca.indeed.com/')


@page_refresh_decorator
def input_search_parameters(browser: webdriver, vacancy_name: str, location_name: str) -> None:
    """Ввести поисковые запросы и перейти к результатам поиска"""
    vacancy_input = browser.find_element(By.CSS_SELECTOR, '#text-input-what')
    vacancy_input.send_keys(vacancy_name)

    location_input = browser.find_element(By.CSS_SELECTOR, '#text-input-where')
    location_input.send_keys(location_name + Keys.ENTER)
    time.sleep(1)

    logger.info(f'Начинаю поиск вакансий "{vacancy_name}" в {location_name}')


def search_result(browser: webdriver) -> bool:
    """Проверить результат выдачи"""
    try:  # Работа с блоком "Вакансии".
        total_vacancies = browser.find_element(By.CSS_SELECTOR,
                                               'div.jobsearch-JobCountAndSortPane-jobCount span').text
        total_vacancies = total_vacancies.split()[0]
        logger.info(f'По запросу найдено вакансий: {total_vacancies}')
        logger.info('Начинаю обход страниц...')
        return True
    except NoSuchElementException:  # Если блока вакансий нет.
        logger.info('Не удалось получить блок "Вакансии"')
        try:  # Работа с блоком "Нет результатов поиска".
            if browser.find_element(By.CSS_SELECTOR,
                                    'div.jobsearch-NoResult-messageContainer').is_displayed():
                logger.info('По данному запросу нет ни одной вакансии')
                return False
        except NoSuchElementException:
            logger.info('Не удалось получить блок "Нет результатов поиска"')


def scrape(browser: webdriver, vacancies: 'Vacancy') -> None:
    """Обойти все страницы поисковой выдачи и добавить вакансии в .html"""
    page_counter = 0  # Счетчик для отслеживания второй страницы выдачи с email рассылкой.

    while True:
        page_counter += 1
        time.sleep(2)

        # Закрытие всплывающего окна с e-mail рассылкой (как правило, на второй странице поисковой выдачи).
        if page_counter == 2:
            try:
                browser.find_element(By.CSS_SELECTOR, 'button[aria-label="close"]').click()
            except NoSuchElementException:
                logger.debug('Не найден блок с e-mail рассылкой')

        # Запись внутреннего HTML-кода объекта в .html файл.
        selenium_jobs_block = browser.find_element(By.CSS_SELECTOR, 'ul.jobsearch-ResultsList')
        selenium_jobs_cards = selenium_jobs_block.find_elements(By.CSS_SELECTOR, 'div.cardOutline')

        for selenium_job_card in selenium_jobs_cards:
            html_job = selenium_job_card.get_attribute('innerHTML')
            vacancies.save_vacancy(html_job)
        logger.info(f'{page_counter}-я страница готова')

        # Перейти на следующую страницу.
        try:
            browser.find_element(By.CSS_SELECTOR, 'nav[role="navigation"] div:last-child a').click()
        except NoSuchElementException:
            logger.info(f'Больше страниц нет')
            break
