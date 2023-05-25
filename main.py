# Встроенный импорт
import os

# Свой импорт
from make_html import make_html
from make_txt import make_txt
from make_csv import make_csv


"""Задать параметры поиска на английском"""
what = 'Python'  # Вакансия
where = 'Calgary'  # Локация


if __name__ == '__main__':
    make_html(what, where)
    html = os.path.exists('./data/temp.html')
    if html:
        make_txt()
        make_csv(what, where)

        """Удалить операционные файлы"""
        os.remove('./data/temp.html')
        os.remove('./data/temp.txt')
        print('Таблица с вакансиями готова')
        print('Временные файлы удалены')
