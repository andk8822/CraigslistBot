import csv
from datetime import datetime
from typing import List

import click

from logger.logger_settings import info_logger, debug_error_logger


VACANCIES_HEADERS = ['#', 'Job title', 'Company', 'Tags', 'Url']  # Заголовки вакансий.


def write(vacancies_list: List[list], vacancy_name: str = '', location_name: str = '', sheet_name: str = 'sheet.csv') -> None:
    """Создать таблицу с вакансиями."""

    # Задать имя.
    if sheet_name == '':
        current_date_time = datetime.now().strftime('%Y-%m-%d at %H-%M')
        sheet_name = f'{vacancy_name} in {location_name} - {len(vacancies_list)} ({current_date_time}).csv'

    # Создать таблицу.
    with open('./csv/' + sheet_name, mode='w', encoding='utf-8', newline='') as sheet:
        writer = csv.writer(sheet)

        writer.writerow(VACANCIES_HEADERS)
        for vacancy in vacancies_list:
            writer.writerow(vacancy)

    info_logger.info('Таблица готова')
