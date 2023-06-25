"""Модуль создает .csv с вакансиями indeed.com"""

import csv
import time
import tempfile
from typing import Optional, List, IO
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


class Run:
    def __init__(self, what: str, where: str, chromedriver_path: str) -> None:
        self._what = what
        self._where = where
        self._chromedriver_path = chromedriver_path

        browser = Browser(self._chromedriver_path).browser
        with tempfile.TemporaryFile(mode='a+', encoding='utf-8') as temp_html:
            Scraper(browser, self._what, self._where, temp_html)
            temp_html.seek(0)
            Parser(self._what, self._where, temp_html)


class Browser:
    """Браузер с настройками"""
    def __init__(self, chromedriver_path: str) -> None:
        self._chromedriver_path = chromedriver_path
        # if chromedriver_path:
        #     self._chromedriver_path = chromedriver_path
        # else:
        #     self._chromedriver_path = './chromedriver/'

        # Первый этап обхода CloudFlare
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')

        # Создать браузер с опциями
        self.browser = webdriver.Chrome(executable_path=self._chromedriver_path, options=options)

        # Второй этап обхода CloudFlare. Удалить маркеры роботизированного ПО из браузера
        self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': """
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            """
        })

        # Задать неявную задержку
        self.browser.implicitly_wait(5)

    def quit(self) -> None:
        """Закрыть браузер"""
        self.browser.quit()


class Scraper:
    """Скрапинг вакансий в .html"""
    def __init__(self, browser: webdriver, what: str, where: str, temp_html: IO) -> None:
        self._browser = browser
        self._what = what
        self._where = where
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
        print(f'Начинаю поиск вакансий "{self._what}" в {self._where}')

    def input_search_parameters(self) -> None:
        """Ввести поисковые запросы и перейти к результатам"""
        what_input = self._browser.find_element(By.CSS_SELECTOR, '#text-input-what')
        what_input.send_keys(self._what)
        time.sleep(1)

        where_input = self._browser.find_element(By.CSS_SELECTOR, '#text-input-where')
        where_input.send_keys(self._where + Keys.ENTER)
        time.sleep(1)

    def search_result(self) -> bool:
        """Проверить результат выдачи"""
        try:  # Работа с блоком "Вакансии"
            total_vacancies = self._browser.find_element(By.CSS_SELECTOR,
                                                         'div.jobsearch-JobCountAndSortPane-jobCount span').text
            total_vacancies = int(total_vacancies.split()[0])
            print(f'По запросу найдено вакансий: {total_vacancies}')
            print('Начинаю сбор вакансий...')
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


class Parser:
    """Парсинг вакансий из .html в .csv"""
    JOBS_DONE: List[list] = [['#', 'Job title', 'Tag', 'Company', 'Rating', 'Url']]  # Шапка для создания .csv

    def __init__(self, what: str, where: str, temp_html: IO) -> None:
        self._what = what
        self._where = where
        self._temp_html = temp_html

        if self._temp_html:
            self.write_csv(self.parse())
        else:
            print("Временный HTML файл не сформирован")

    def parse(self) -> List[list]:
        """Парсинг временного html-файла"""
        soup = BeautifulSoup(self._temp_html, 'lxml')

        jobs_raw = soup.find_all(class_='job_seen_beacon')  # HTML список с вакансиями. Объект Beautiful Soup
        vacancy_counter = 0  # Счетчик вакансий

        # Обойти html блоки, добавить их во временный список и в итоге все списки добавить в один
        for job in jobs_raw:
            temp = list()  # Временный список-конструктор вакансии
            vacancy_counter += 1  # Счетчик вакансий

            # Добавить номер вакансии
            temp.append(vacancy_counter)

            # Добавить должность
            job_title = job.find('h2').find('span').text
            temp.append(job_title)

            # Добавить тег если имеется
            try:
                tags_list = list()
                tags = job.find('div', class_='metadata').find_all(class_='attribute_snippet')
                for tag in tags:
                    tags_list.append(tag.text)
                if tags_list:
                    temp.append(*tags_list)
                else:
                    raise
            except AttributeError:
                temp.append('No tags')

            # Добавить компанию
            company = job.find('span', class_='companyName').text
            temp.append(company)

            # Добавить рейтинг indeed если имеется
            try:
                rating = job.find('span', class_='ratingNumber').find('span').text
                temp.append(rating)
            except AttributeError:
                temp.append('No rating')

            # Добавить ссылку
            url = 'https://ca.indeed.com' + job.find('h2').find('a')['href']
            temp.append(url)

            # Добавить готовую вакансию в финальный список
            self.JOBS_DONE.append(temp)
        return self.JOBS_DONE

    def write_csv(self, jobs_list: List[list]) -> None:
        """Создать .csv из list()"""

        # Имя в формате вакансия_в_локация_текущая_дата
        now = datetime.now()
        current_time = now.strftime('%Y-%m-%d-%H-%M')
        name_with_current_time = f'{self._what} in {self._where} ({current_time}).csv'

        # Создание и запись .csv
        with open('./csv/' + name_with_current_time, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)

            for job in jobs_list:
                writer.writerow(job)

        print('Таблица с вакансиями готова')
