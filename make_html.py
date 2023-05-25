# Встроенные импорт
import time

# Сторонний импорт
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


chromedriver_path = './chromedriver/'


def make_html(what, where):
    """Функция парсит url-страницы и добавляет html блоки вакансий в html файл"""

    try:
        """Первый этап обхода CloudFlare"""
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')

        """Создать браузер с опциями"""
        browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)

        """Второй этап обхода CloudFlare. Удалить маркеры роботизированного ПО из браузера"""
        browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': """
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            """
        })

        """Задать неявную задержку"""
        browser.implicitly_wait(5)

        """Перейти на сайт"""
        browser.get(f'https://ca.indeed.com/')
        print(f'Начинаю поиск вакансий "{what}" в {where}')

        """Ввести вакансию"""
        what_input = browser.find_element(By.CSS_SELECTOR, '#text-input-what')
        what_input.send_keys(what)
        time.sleep(1)

        """Ввести локацию и перейти к результатам поиска"""
        where_input = browser.find_element(By.CSS_SELECTOR, '#text-input-where')
        where_input.send_keys(where + Keys.ENTER)
        time.sleep(1)

        """Проверить наличие результатов выдачи"""
        try:
            if browser.find_element(By.CSS_SELECTOR, 'div.jobsearch-NoResult-messageContainer').is_displayed():
                print('По данному запросу нет ни одной вакансии')
                return
        except:
            pass

        """Определить количество страниц поискового запроса"""
        total_vacancies = browser.find_element(By.CSS_SELECTOR, 'div.jobsearch-JobCountAndSortPane-jobCount span').text
        total_vacancies = int(total_vacancies.split()[0])
        print(f'По запросу найдено вакансий: {total_vacancies}')
        print('Начинаю сбор вакансий...')

        """Обходим все страницы поисковой выдачи"""
        page_counter = 0  # Счетчик для отслеживания второй страницы выдачи с email рассылкой
        while True:
            page_counter += 1
            """Явная задержка"""
            time.sleep(2)

            """Закрытие всплывающего окна с e-mail рассылкой (как правило на второй странице поисковой выдачи)"""
            if page_counter == 2:  # Без счетчика browser.implicity_wait(5) замедляет обход каждой стр. на 5 секунд
                try:
                    browser.find_element(By.CSS_SELECTOR, 'button[aria-label="close"]').click()
                except:
                    pass

            """Дозапись внутреннего HTML-кода объекта в .html файл"""
            result = browser.find_element(By.CSS_SELECTOR, '#mosaic-jobResults ul')
            result = result.get_attribute('innerHTML')
            with open('./data/temp.html', mode='a', encoding='utf-8') as file:
                file.write(result)
                file.write('\n')
            print(f'{page_counter}-я страница готова')

            try:
                """Перейти на следующую страницу"""
                browser.find_element(By.CSS_SELECTOR, 'nav[role="navigation"] div:last-child a').click()
            except:
                print(f'Больше страниц нет')
                break
        print('HTML файл готов')
    finally:
        time.sleep(1)
        browser.quit()
