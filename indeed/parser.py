from typing import List, Tuple

from bs4 import BeautifulSoup


class Vacancy:

    def __init__(self):
        self.vacancies: List[list] = list()

    @property
    def get_vacancies(self) -> List[list]:
        """Получить список со списком вакансий."""
        return self.vacancies

    def save_vacancy(self, vacancy_html: str) -> None:
        """Добавить список с элементами вакансии в список с вакансиями."""
        vacancy: List = self._parse_vacancy(vacancy_html)
        self.vacancies.append(vacancy)

    def _parse_vacancy(self, vacancy_html: str) -> list:
        """Разобрать вакансию в формате html на элементы списка."""
        soup = BeautifulSoup(vacancy_html, 'lxml')
        temp_vacancy_elements = list()

        # Добавить порядковый номер вакансии
        if len(self.vacancies) > 0:
            temp_vacancy_elements.append(self.vacancies[-1][0] + 1)
        else:
            temp_vacancy_elements.append(1)

        # Добавить должность
        job_title = soup.find('h2').find('span').text
        temp_vacancy_elements.append(job_title)

        # Добавить компанию.
        company = soup.find('span', class_='companyName').text
        temp_vacancy_elements.append(company)

        # Добавить тег если имеется.
        try:
            tags_list = list()
            tags = soup.find_all('div', class_='attribute_snippet')
            for tag in tags:
                tag_str = tag.text
                if '+' in tag_str[-3:]:
                    tags_list.append(tag_str[:tag_str.rfind('+')].rstrip())
                else:
                    tags_list.append(tag_str)
            if tags_list:
                tags_str = '. '.join(str(i).strip().capitalize() for i in tags_list)  # Все теги в одну строку.
                temp_vacancy_elements.append(tags_str)
            else:
                raise AttributeError
        except AttributeError:  # Если нет блока тегов.
            temp_vacancy_elements.append('No tags')

        # Добавить ссылку
        url = 'https://ca.indeed.com' + soup.find('h2').find('a')['href']
        temp_vacancy_elements.append(url)

        return temp_vacancy_elements
