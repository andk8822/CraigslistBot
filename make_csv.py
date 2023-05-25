# Встроенные модули
import csv
from datetime import datetime


def make_csv(what, where):
    """Функция создает финальный .csv из .txt с собранными вакансиями"""

    now = datetime.now()
    time = now.strftime('%Y-%m-%d-%H-%M')

    name_with_time = f'{what} in {where} ({time}).csv'  # Имя в формате вакансия_в_локация_текущая_дата

    """Каждые 6 строк из .txt записать в отдельные ячейки одного ряда .csv"""
    with open('./data/temp.txt', mode='r', encoding='utf-8') as file_in,\
            open('./data/'+name_with_time, mode='w', encoding='utf-8', newline='') as file_out:
        text = file_in.readlines()
        writer = csv.writer(file_out)

        row = list()

        for line in text:
            row.append(line.strip())

            if len(row) == 6:
                writer.writerow(row)
                row = list()

        if row:
            writer.writerow(row)
