from typing import List

from indeed.parser import parse_html_vacancy, Vacancy


def test_parser_vacancy_class(vacancies_html: List[str]):
    """Тест на парсинг html-блоков из списка."""
    counter: int = 0

    for vacancy_html in vacancies_html:
        counter += 1
        vacancy = parse_html_vacancy(vacancy_html)

        assert isinstance(vacancy, Vacancy)
        assert isinstance(vacancy.job_title, str)
        assert isinstance(vacancy.company_name, str)
        assert isinstance(vacancy.tags, str)
        assert isinstance(vacancy.url, str)

    assert counter == len(vacancies_html), 'Парсер обработал не все html-вакансии.'
