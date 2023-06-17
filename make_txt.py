from bs4 import BeautifulSoup


def make_txt():
    """Функция парсит страницу и создает txt-файл с вакансиями"""

    """Открыть .html файл"""
    with open('./data/temp.html') as file:
        soup = BeautifulSoup(file, 'lxml')

    jobs_done = [['#', 'Job title', 'Tag', 'Company', 'Rating', 'Url']]  # Финальный список вакансий с шапкой
    jobs_raw = soup.find_all(class_='job_seen_beacon')  # HTML список с вакансиями. Объект Beautiful Soup
    vacancy_counter = 0  # Счетчик вакансий

    """Обойти html блоки, добавить их в временный список и в итоге все списки добавить в один"""
    for job in jobs_raw:
        temp = list()  # Временный список-конструктор вакансии
        vacancy_counter += 1  # Счетчик вакансий

        """Добавить номер вакансии"""
        temp.append(vacancy_counter)

        """Добавить должность"""
        job_title = job.find('h2').find('span').text
        temp.append(job_title)

        """Добавить тег"""
        try:
            tags_list = list()
            tags = job.find('div', class_='metadata').find_all(class_='attribute_snippet')
            for tag in tags:
                tags_list.append(tag.text)
            if tags_list:
                temp.append(*tags_list)
            else:
                raise
        except:
            temp.append('No tags')

        """Добавить компанию"""
        company = job.find('span', class_='companyName').text
        temp.append(company)

        """Добавить рейтинг"""
        try:
            rating = job.find('span', class_='ratingNumber').find('span').text
            temp.append(rating)
        except:
            temp.append('No rating')

        """Добавить ссылку"""
        url = 'https://ca.indeed.com' + job.find('h2').find('a')['href']
        temp.append(url)

        """Добавить готовую вакансию в финальный список"""
        jobs_done.append(temp)

    """Запись списка с вакансиями в .txt файл"""
    with open('./data/temp.txt', mode='w', encoding='utf-8') as file:
        for vacancy in jobs_done:
            for element in vacancy:
                file.write(str(element) + '\n')
    print('TXT файл готов')
