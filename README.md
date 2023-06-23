# Indeed parser

---
### Описание
Данный проект собирает все вакансии начиная с самой свежей по указанному запросу
в требуемой локации внутри Канады с сайта [indeed.com](https://indeed.com) и
помещает результат в csv таблицу. В таблице вакансия распределяется по столбцам:
порядковый номер вакансии, ее название, тег (если есть), название компании,
ее рейтинг от indeed.com (если есть), ссылку на вакансию.

### Установка и настройка
Установите проект, создайте и активируйте виртуальное окружение, установите все требуемые зависимости из файла `requirements.txt`
установите браузер Google Chrome на ваш ПК (если его еще нет),
[скачайте](https://chromedriver.chromium.org/downloads) `cromedriver.exe` который
соответствует версии вашего Google Chrome и поместить его в папку "./cromedriver"
внутри проекта.

### Использование
Откройте `main.py` и в переменных "what" и "where" укажите вакансию и локацию по
которой будет производиться поиск. Запустите файл. После того как программа 
отработает внутри проекта в каталоге "./data" появится .csv файл с именем
"вакансия in локация (гггг-мм-дд-чч-мин)", а временные файлы будут удалены.
В таблице с результатами вакансий может быть меньше чем заявляет сам indeed.com
так как он же и не отображает дубли в поисковой выдаче.

### Автор
Андрей Калинкин  
email: andk.8822@gmail.com