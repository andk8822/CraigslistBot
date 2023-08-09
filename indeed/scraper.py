import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from logger.logger_settings import info_logger, debug_error_logger


class Scraper:
    def __init__(self, browser: webdriver):
        self._browser = browser
        self._vacancies: list = list()
        self._page: int = 0
        self._run()

    @property
    def get_vacancies(self) -> list:
        """Получить список со списком вакансий."""
        return self._vacancies

    @property
    def get_page(self) -> int:
        """Получить количество страниц"""
        return self._page

    def _run(self) -> None:
        """Скрапинг вакансий."""
        self._scrape()

    def _page_counter(self) -> int:
        """Счетчик для отслеживания второй страницы выдачи с email рассылкой."""
        self._page += 1
        return self._page

    def _close_authorization_via_services_window(self) -> None:
        """Закрытие окна авторизации через сервисы Google & Apple"""
        if self._page == 2:
            try:
                self._browser.find_element(By.CSS_SELECTOR, 'button[id="passport-modal-overlay-social-onetap-modal-close'
                                                            '-button"').click()
                info_logger.info('Закрытие окна "Авторизация с помощью сервисов"')
            except NoSuchElementException:
                info_logger.info('Не найдено окно "Авторизация с помощью сервисов"')

    def _close_email_window(self) -> None:
        """Закрытие окна email-рассылки."""
        if self._page == 2:
            try:
                self._browser.find_element(By.CSS_SELECTOR, 'button[aria-label="close"]').click()
                info_logger.info('Закрытие окна e-mail рассылки')
            except NoSuchElementException:
                info_logger.info('Не найдено окно с e-mail рассылкой')

    def _scrape(self):
        """Скрапинг html-блоков на странице."""
        while True:
            self._page_counter()
            time.sleep(2)
            self._close_authorization_via_services_window()
            self._close_email_window()

            selenium_jobs_block = self._browser.find_element(By.CSS_SELECTOR, 'ul.jobsearch-ResultsList')
            selenium_jobs_cards = selenium_jobs_block.find_elements(By.CSS_SELECTOR, 'div.cardOutline')

            for selenium_job_card in selenium_jobs_cards:
                html_job = selenium_job_card.get_attribute('innerHTML')
                self._vacancies.append(html_job)
            info_logger.info(f'{self._page}-я страница готова')

            if not self._go_to_next_page():
                break

    def _go_to_next_page(self) -> bool:
        """Перейти на следующую страницу."""
        try:
            self._browser.find_element(By.CSS_SELECTOR, 'nav[role="navigation"] div:last-child a').click()
            return True
        except NoSuchElementException:
            info_logger.info(f'Больше страниц нет')
            return False


def go_to_site(browser: webdriver, url: str = 'https://ca.indeed.com/') -> None:
    """Перейти на сайт"""
    browser.get(url)


def page_refresh_decorator(number_of_attempts: int = 2):  # Callable[[Callable], Callable]
    """Декоратор для перезагрузки страницы при ошибке NoSuchElementException"""

    def decorator(func):
        def wrapper(browser, vacancy_name, location_name):
            for i in range(1, number_of_attempts + 1):
                try:
                    func(browser, vacancy_name, location_name)
                    break
                except NoSuchElementException:
                    info_logger.info(f'Элемент не найден. Попытка перезагрузки страницы {i}/{number_of_attempts}')
                    debug_error_logger.debug(f'Элемент не найден. Попытка перезагрузки страницы {i}/{number_of_attempts}')
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

    info_logger.info(f'Начинаю поиск вакансий "{vacancy_name}" в {location_name}')


def check_result(browser: webdriver) -> bool:
    """Проверить результат выдачи"""
    try:  # Работа с блоком "Вакансии".
        total_vacancies = browser.find_element(By.CSS_SELECTOR,
                                               'div.jobsearch-JobCountAndSortPane-jobCount span').text
        total_vacancies = total_vacancies.split()[0]
        info_logger.info(f'По запросу найдено вакансий: {total_vacancies}')
        return True
    except NoSuchElementException:  # Если блока "Вакансии" нет.
        info_logger.info('Не удалось получить блок "Вакансии"')
        try:  # Работа с блоком "Нет результатов поиска".
            if browser.find_element(By.CSS_SELECTOR,
                                    'div.jobsearch-NoResult-messageContainer').is_displayed():
                info_logger.info('По данному запросу нет ни одной вакансии')
                return False
        except NoSuchElementException:
            info_logger.info('Проблемы с доступом к сайту. Не удалось получить блок "Нет результатов поиска"')
