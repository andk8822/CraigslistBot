from typing import Union

import click

from indeed import Run


@click.command()
@click.option('--what', default='Barber', help='Vacancy to search', type=Union[str, int])
@click.option('--where', default='Calgary', help='Place to search', type=str)
@click.option('--chromedriver_path', '-cp', default='./chromedriver/', help='Path to chromedriver', type=str)
def main(what: Union[str, int], where: str, chromedriver_path: str) -> None:
    """Создать csv-таблицу вакансий с сайта ca.indeed.com по заданным параметрам поиска"""
    if what and where:
        Run(what, where, chromedriver_path)
    else:
        raise AttributeError('Необходимо ввести поисковые запросы "вакансия", "локация"!')


if __name__ == "__main__":
    main()
