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

    # @click.command()
    # @click.option('--sheet_name', default=None, prompt='Введите имя для таблицы:', help='Имя для таблицы')
    # def get_csv(self, sheet_name: str) -> None:
    #     """Создать .csv"""
    #
    #     # Задать имя
    #     if sheet_name is None:
    #         current_date_time = datetime.now().strftime('%Y-%m-%d at %H-%M')
    #         sheet_name = f'{self._vacancy_name} in {self._location_name} - {len(self.vacancies)} ({current_date_time}).csv'
    #
    #     # Запись
    #     with open('./csv/' + sheet_name, mode='w', encoding='utf-8', newline='') as sheet:
    #         writer = csv.writer(sheet)
    #
    #         writer.writerow(self._VACANCIES_HEADERS)
    #         for vacancy in self.vacancies:
    #             writer.writerow(vacancy)

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

        # Добавить компанию
        company = soup.find('span', class_='companyName').text
        temp_vacancy_elements.append(company)

        # Добавить тег если имеется
        try:
            tags_list = list()
            tags = soup.find_all('div', class_='attribute_snippet')
            for tag in tags:
                tags_list.append(tag.text)

            if tags_list:
                tags_str = '. '.join(str(i).strip().capitalize() for i in tags_list)
                temp_vacancy_elements.append(tags_str)
            else:  # Если список тегов пустой
                raise AttributeError
        except AttributeError:
            temp_vacancy_elements.append('No tags')
        # Правильно я понимаю, что в строке с кодом `raise` произойдет переключение на блок except?

        # Добавить рейтинг indeed если имеется
        try:
            rating = float(soup.find('span', class_='ratingNumber').find('span').text)
            temp_vacancy_elements.append(rating)
        except AttributeError:
            temp_vacancy_elements.append('No rating')

        # Добавить ссылку
        url = 'https://ca.indeed.com' + soup.find('h2').find('a')['href']
        temp_vacancy_elements.append(url)

        return temp_vacancy_elements
