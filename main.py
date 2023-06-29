from typing import Union

import click

from indeed.run import Run


@click.command()
@click.option('--what', default='Barber', prompt='Введите вакансию', help='Поиск вакансии')
@click.option('--where', default='Calgary', prompt='Введите локацию', help='Поиск локации')
@click.option('--chromedriver_path', default='./chromedriver/', help='Папка с chromedriver')
def run_indeed(what: Union[str, int], where: str, chromedriver_path: str) -> None:
    """Создать csv-таблицу вакансий с сайта ca.indeed.com по заданным параметрам поиска"""
    Run(what, where, chromedriver_path)


if __name__ == "__main__":
    run_indeed()
