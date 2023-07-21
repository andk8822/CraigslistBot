import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from indeed.logger_settings import logger


def go_to_site(browser: webdriver) -> None:
    """Перейти на сайт"""
    browser.get('https://ca.indeed.com/')


def page_refresh_decorator(attempt: int = 2):
    """Декоратор для перезагрузки страницы при ошибке NoSuchElementException"""

    def decorator(func):
        def wrapper(browser, vacancy_name, location_name):
            for i in range(1, attempt + 1):
                try:
                    func(browser, vacancy_name, location_name)
                    break
                except NoSuchElementException:
                    logger.info(f'Элемент не найден. Попытка перезагрузки страницы {i}/{attempt}')
                    logger.debug(f'Элемент не найден. Попытка перезагрузки страницы {i}/{attempt}')
                    browser.refresh()

        return wrapper

    return decorator


@page_refresh_decorator()
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
    except NoSuchElementException:  # Если блока "Вакансии" нет.
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
                logger.info('Закрытие окна e-mail рассылки')
            except NoSuchElementException:
                logger.debug('Не найден блок с e-mail рассылкой')

        # Запись внутреннего HTML-кода объекта в html-файл.
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
