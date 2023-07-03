import click

from indeed.run import Run


@click.command()
@click.option('--vacancy', default='Barber', prompt='Введите вакансию', help='Поиск вакансии')
@click.option('--location', default='Calgary', prompt='Введите локацию', help='Поиск локации')
@click.option('--chromedriver_path', default='./chromedriver/', help='Папка с chromedriver')
def run_indeed(vacancy: str, location: str, chromedriver_path: str) -> None:
    """Создать csv-таблицу вакансий с сайта ca.indeed.com по заданным параметрам поиска"""
    Run(vacancy, location, chromedriver_path)


if __name__ == "__main__":
    run_indeed()
