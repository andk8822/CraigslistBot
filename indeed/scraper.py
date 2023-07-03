import time
from typing import IO

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class Scraper:
    """Скрапинг вакансий в .html"""
    def __init__(self, browser: webdriver, vacancy: str, location: str, temp_html: IO) -> None:
        self._browser = browser
        self._vacancy = vacancy
        self._location = location
        self._temp_html = temp_html

        self.go_to_site()
        self.input_search_parameters()
        if self.search_result():
            self.scrape()
            self._browser.quit()
        else:
            self._browser.quit()

    def go_to_site(self) -> None:
        """Перейти на сайт"""
        self._browser.get('https://ca.indeed.com/')
        print(f'Начинаю поиск вакансий "{self._vacancy}" в {self._location}')

    def input_search_parameters(self) -> None:
        """Ввести поисковые запросы и перейти к результатам"""
        vacancy_input = self._browser.find_element(By.CSS_SELECTOR, '#text-input-what')
        vacancy_input.send_keys(self._vacancy)
        time.sleep(1)

        location_input = self._browser.find_element(By.CSS_SELECTOR, '#text-input-where')
        location_input.send_keys(self._location + Keys.ENTER)
        time.sleep(1)

    def search_result(self) -> bool:
        """Проверить результат выдачи"""
        try:  # Работа с блоком "Вакансии"
            total_vacancies = self._browser.find_element(By.CSS_SELECTOR,
                                                         'div.jobsearch-JobCountAndSortPane-jobCount span').text
            total_vacancies = int(total_vacancies.split()[0])
            print(f'По запросу найдено вакансий: {total_vacancies}')
            print('Начинаю обход страниц...')
            return True
        except NoSuchElementException:  # Если блока вакансий нет
            print('Не удалось получить блок "Вакансии"')
            try:  # Работа с блоком "Нет результатов поиска"
                if self._browser.find_element(By.CSS_SELECTOR,
                                              'div.jobsearch-NoResult-messageContainer').is_displayed():
                    print('По данному запросу нет ни одной вакансии')
                    return False
            except NoSuchElementException:
                print('Не удалось получить блок "Нет результатов поиска"')

    def scrape(self) -> None:
        """Обойти все страницы поисковой выдачи и добавить вакансии в .html"""
        page_counter = 0  # Счетчик для отслеживания второй страницы выдачи с email рассылкой

        while True:
            page_counter += 1
            time.sleep(2)

            # Закрытие всплывающего окна с e-mail рассылкой (как правило, на второй странице поисковой выдачи)
            if page_counter == 2:
                try:
                    self._browser.find_element(By.CSS_SELECTOR, 'button[aria-label="close"]').click()
                except NoSuchElementException:
                    print('Не найден блок с e-mail рассылкой')

            # Запись внутреннего HTML-кода объекта в .html файл
            html_block = self._browser.find_element(By.CSS_SELECTOR, '#mosaic-jobResults ul')
            html_block = html_block.get_attribute('innerHTML')
            self.write_html(html_block)
            print(f'{page_counter}-я страница готова')

            # Перейти на следующую страницу
            try:
                self._browser.find_element(By.CSS_SELECTOR, 'nav[role="navigation"] div:last-child a').click()
            except NoSuchElementException:
                print(f'Больше страниц нет')
                break

        print('HTML файл готов')

    def write_html(self, html_block: str) -> None:
        """Запись html-блока во временный файл"""
        self._temp_html.write(html_block)
        self._temp_html.write('\n')
