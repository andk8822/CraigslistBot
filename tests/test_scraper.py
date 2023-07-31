from selenium.webdriver.common.by import By

from indeed import scraper


def test_go_to_site(browser):
    """Переход на сайт https://ca.indeed.com/"""
    expected = 'https://ca.indeed.com/'
    scraper.go_to_site(browser)
    assert browser.current_url == expected, f'Текущий адрес не соответствует {expected}'


class TestInputSearchParameters:
    """Страница ввода поисковых запросов"""
    def test_vacancy_input_field(self, browser):
        vacancy_input_is_displayed = browser.find_element(By.CSS_SELECTOR, '#text-input-what').is_displayed()
        vacancy_input_is_enabled = browser.find_element(By.CSS_SELECTOR, '#text-input-what').is_enabled()
        assert vacancy_input_is_displayed is True, 'Поле для ввода вакансии не отображается'
        assert vacancy_input_is_enabled is True, 'Поле для ввода вакансии не активно'

    def test_location_input_field(self, browser):
        location_input_is_displayed = browser.find_element(By.CSS_SELECTOR, '#text-input-where').is_displayed()
        location_input_is_enabled = browser.find_element(By.CSS_SELECTOR, '#text-input-where').is_enabled()
        assert location_input_is_displayed is True, 'Поле для ввода локации не отображается'
        assert location_input_is_enabled is True, 'Поле для ввода локации не активно'

    def test_search_button(self, browser):
        find_jobs_button_is_displayed = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').is_displayed()
        find_jobs_button_is_enabled = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').is_enabled()
        assert find_jobs_button_is_displayed is True, 'Кнопка "Find jobs" не отображается'
        assert find_jobs_button_is_enabled is True, 'Кнопка "Find jobs" не активна'


# class TestSearchResult:
#     """Результат поисковой выдачи"""

#     Нужно получить 3 страницы:
#     - Вакансии есть по запросу.
#     - Вакансии есть без запроса.
#     - Вакансий нет по запросу.

#     vacancy_name = 'Barber'
#     location_name = 'Calgary'
#     scraper.input_search_parameters(test_browser, vacancy_name, location_name)
#     pass


# Test scraper function
