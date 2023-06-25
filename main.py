from typing import Union

import click

from indeed import Run


@click.command()
@click.option('--what', prompt='Enter vacancy', help='Vacancy to search')
@click.option('--where', prompt='Enter location', help='Location to search')
@click.option('--chromedriver_path', default='./chromedriver/', help='Path to chromedriver')
def main(what: Union[str, int], where: str, chromedriver_path: str) -> None:
    """Создать csv-таблицу вакансий с сайта ca.indeed.com по заданным параметрам поиска"""
    if what and where:
        Run(what, where, chromedriver_path)
    else:
        raise AttributeError('Необходимо ввести поисковые запросы "вакансия", "локация"!')


if __name__ == "__main__":
    main()
