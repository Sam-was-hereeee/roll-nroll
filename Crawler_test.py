import requests
from bs4 import BeautifulSoup

f = open("courses.txt", mode='wt', encoding='utf-8')
f.close()
f = open("courses.txt", mode='a', encoding='utf-8')
class Crawler:
    def __init__(self):
        self.url = 'https://nol.ntu.edu.tw/nol/coursesearch/search_result.php?current_sem=112-2&cstype=1&csname=&alltime=yes&allproced=yes&allsel=yes&page_cnt=15&Submit22=%E6%9F%A5%E8%A9%A2'
        self.soup = BeautifulSoup(requests.get(self.url).text, 'html.parser')
        self.course_list = (self.soup.find_all("table", {"border": "1"})[1]).findAll("tr")

    def go_next_page(self):
        last_table = self.soup.find_all("table")[-1]
        next_page = str(last_table.find_all("a")[-1]["href"])
        print(str(next_page))
        self.url = self.url + next_page
        print(self.url)
        self.soup = BeautifulSoup(requests.get(self.url).text, 'html.parser')
        self.course_list = (self.soup.find_all("table", {"border": "1"})[1]).findAll("tr")
        print(self.course_list)

    def export_current_page(self):
        for course in self.course_list[1:]:
            for data in course.find_all("td"):
                f.write(data.text + ' ')
            f.write('\n')


class Course:
    def __init__(self, souped_course):
        pass


crawler = Crawler()

crawler.export_current_page()
crawler.go_next_page()
crawler.export_current_page()

s = requests.session()
s.headers = {'User-Agent': 'Mozilla/5.0'}
baseUrl = "https://nol.ntu.edu.tw/nol/coursesearch/search_result.php"
url = 'https://nol.ntu.edu.tw/nol/coursesearch/search_result.php?current_sem=112-2&cstype=1&csname=&alltime=yes&allproced=yes&allsel=yes&page_cnt=15&Submit22=%E6%9F%A5%E8%A9%A2'
response = requests.get(url)
# print(response.text)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.findAll("table", {"border": "1"})
last_table = soup.find_all("table")[-1]
rows = tables[1].findAll("tr")

# print(last_table)
next_page = str(last_table.find_all("a")[-1]["href"])