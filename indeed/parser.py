import csv
from datetime import datetime
from typing import List, IO

from bs4 import BeautifulSoup


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

        # Имя в формате количество_вакансия_в_локация_текущая_дата_время
        total_vacancies = str(len(jobs_list)-1)
        current_date_time = datetime.now().strftime('%Y-%m-%d-%H-%M')
        file_name = f'{total_vacancies} {self._what} in {self._where} ({current_date_time}).csv'

        # Создание и запись .csv
        with open('./csv/' + file_name, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)

            for job in jobs_list:
                writer.writerow(job)

        print('Таблица с вакансиями готова')
