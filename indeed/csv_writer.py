import csv
from datetime import datetime
from typing import List

import click

from logger.logger_settings import info_logger, debug_error_logger
from indeed.parser import Vacancy


VACANCIES_HEADERS = ['Job title', 'Company', 'Tags', 'Url']  # Заголовки вакансий.


def write(vacancies_ready: List[Vacancy], vacancy_name: str = '', location_name: str = '', sheet_name: str = 'sheet.csv') -> None:
    """Создать таблицу с вакансиями."""

    # Задать имя.
    if sheet_name == '':
        current_date_time = datetime.now().strftime('%Y-%m-%d at %H-%M')
        sheet_name = f'{vacancy_name} in {location_name} - {len(vacancies_ready)} ({current_date_time}).csv'

    # Создать таблицу.
    with open('./csv/' + sheet_name, mode='w', encoding='utf-8', newline='') as sheet:
        writer = csv.writer(sheet)

        writer.writerow(VACANCIES_HEADERS)
        for vacancy in vacancies_ready:
            writer.writerow([vacancy.job_title, vacancy.company_name, vacancy.tags, vacancy.url])

    info_logger.info('Таблица готова')
