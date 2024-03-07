# Indeed parser

---
### Description
This project collects all job openings starting with the most recent one for a given request
in the required location within Canada from [ca.indeed.com](https://ca.indeed.com) and
puts the result into a csv table. The table categorizes the vacancy into columns:
job sequence number, job title, tag (if any), company name,
its rating from ca.indeed.com (if any), link to the vacancy.

### Installation
Install the project, create and activate the virtual environment,
install all required dependencies from the `requirements.txt` file
install Google Chrome browser on your PC (if you don't already have it),
[download](https://chromedriver.chromium.org/downloads) `cromedriver.exe` which
matches the version of your Google Chrome and place it in the folder "./cromedriver"
inside the project.

### Usage
In the console, run `main.py` and follow the prompts to enter search terms.
After the program exit, a csv file wi;; be created with the name "number_vacancies vacancy in location (yyyy-mm-dd-hh-mmm)".
a csv file with the name "number_vacancies vacancy vacancy in location (yyyyyy-mm-dd-dd-hh-min)" will appear in the "./csv" directory.
There may be fewer vacancies in the table with results than ca.indeed.com itself states
as it does not show duplicates in the search results.

### Author
Andrii Kalinkin
email: andriikalinkin@gmail.com
