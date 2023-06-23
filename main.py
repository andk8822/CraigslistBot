from indeed import Run


def main() -> None:
    """Создать .csv вакансий с indeed.com по заданным параметрам поиска"""

    """Задать параметры скрапинга"""  # Этому здесь не место
    what: str = 'Barber'  # Вакансия
    where: str = 'Calgary'  # Локация

    """Получить .csv с вакансиями"""
    Run(None, what, where)

    """Удалить операционные файлы"""  # Этому здесь не место
    # os.remove('./csv/temp.html')
    # print('Таблица с вакансиями готова')
    # print('Временные файлы удалены')


if __name__ == "__main__":
    main()