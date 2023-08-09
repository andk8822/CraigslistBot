"""Все функции, представленные в данном файле зависят друг от друга и требуют соблюдения установленной очередности."""
from selenium import webdriver
from selenium.webdriver.common.by import By

from indeed import scraper


def test_go_to_site(browser: webdriver):
    """Тест перехода на сайт https://ca.indeed.com/"""
    expected = 'https://ca.indeed.com/'
    scraper.go_to_site(browser)
    assert browser.current_url == expected, f'Текущий адрес не соответствует {expected}'


def test_vacancy_input_field(browser: webdriver):
    """Тест поля ввода вакансии"""
    vacancy_input_is_displayed = browser.find_element(By.CSS_SELECTOR, '#text-input-what').is_displayed()
    vacancy_input_is_enabled = browser.find_element(By.CSS_SELECTOR, '#text-input-what').is_enabled()
    assert vacancy_input_is_displayed is True, 'Поле для ввода вакансии не отображается'
    assert vacancy_input_is_enabled is True, 'Поле для ввода вакансии не активно'


def test_location_input_field(browser: webdriver):
    """Тест поля ввода результата"""
    location_input_is_displayed = browser.find_element(By.CSS_SELECTOR, '#text-input-where').is_displayed()
    location_input_is_enabled = browser.find_element(By.CSS_SELECTOR, '#text-input-where').is_enabled()
    assert location_input_is_displayed is True, 'Поле для ввода локации не отображается'
    assert location_input_is_enabled is True, 'Поле для ввода локации не активно'


def test_search_button(browser: webdriver):
    """Тест кнопки поиска"""
    find_jobs_button_is_displayed = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').is_displayed()
    find_jobs_button_is_enabled = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').is_enabled()
    assert find_jobs_button_is_displayed is True, 'Кнопка "Find jobs" не отображается'
    assert find_jobs_button_is_enabled is True, 'Кнопка "Find jobs" не активна'


def test_search_result(browser: webdriver):
    """Тест наличия результатов поисковой выдачи"""
    # Ввести поисковые запросы
    scraper.input_search_parameters(browser, 'Python Junior', 'Calgary')
    assert scraper.check_result(browser), 'Нет результатов поисковой выдачи'


def test_scraper_class(browser: webdriver):
    """Тест класса Scraper и всей его логики"""
    vacancies_list_with_htmls = scraper.Scraper(browser).get_vacancies
    assert len(vacancies_list_with_htmls) > 0, 'Список вакансий пуст'
