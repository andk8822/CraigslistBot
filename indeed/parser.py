from dataclasses import dataclass

from bs4 import BeautifulSoup


@dataclass
class Vacancy:
    job_title: str
    company_name: str
    tags: str
    url: str


def parse_html_vacancy(vacancy_html: str) -> Vacancy:
    """Распарсить html-вакансию и вернуть как объект класса Vacancy"""
    soup = BeautifulSoup(vacancy_html, 'lxml')

    # Должность
    job_title = soup.find('h2').find('span').text

    # Компания
    company_name = soup.find('span', class_='companyName').text

    # Теги, если имеются
    try:
        tags_list: list = list()
        tags_html = soup.find_all('div', class_='attribute_snippet')

        for tag_html in tags_html:
            tag_str = tag_html.text
            if '+' in tag_str[-3:]:
                tags_list.append(tag_str[:tag_str.rfind('+')].rstrip())
            else:
                tags_list.append(tag_str)
        if tags_list:
            tags_string = '. '.join(str(i).strip().capitalize() for i in tags_list)  # Все теги в одну строку.
        else:
            raise AttributeError
    except AttributeError:  # Если нет блока тегов.
        tags_string = 'No tags'
    # Ссылка
    url = 'https://ca.indeed.com' + soup.find('h2').find('a')['href']

    return Vacancy(job_title, company_name, tags_string, url)
