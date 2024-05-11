from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

f = open("courses_selenium.txt", mode='wt', encoding='utf-8')
f.close()
f = open("courses_selenium.txt", mode='a', encoding='utf-8')

class Crawler:
    html = ""
    soup = None
    course_list = None
    button = None
    current_page = 1
    link_dict = {}
    course_current_id = 0

    def __init__(self):
        self.s = Service(r'C:\Vitrual_D_Disk\programming_practice\ccClub\Project\msedgedriver.exe')
        self.driver = webdriver.ChromiumEdge(service=self.s)
        self.driver.get("https://nol.ntu.edu.tw/nol/coursesearch/search_result.php?current_sem=112-2&cstype=1&csname=&alltime=yes&allproced=yes&allsel=yes&page_cnt=8000&Submit22=%E6%9F%A5%E8%A9%A2")

    def scrape_course_list(self):
        self.html = self.driver.page_source
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.course_list = (self.soup.find_all("table", {"border": "1"})[1]).findAll("tr")

    def export_course_list(self):
        course_text = []
        for course in self.course_list[1:]:
            course_text.append(str(self.course_current_id))
            self.course_current_id += 1
            for c, data in enumerate(course.find_all("td")):
                course_text.append(data.text)
                if c == 4:
                    try:
                        link = data.a['href']
                        course_text.append(str(link))
                    except TypeError:
                        course_text.append("no_link")
            course_text.append('\n')
        course_text = '/'.join(course_text)
        course_text = course_text.replace('\n/', '\n')
        f.write(course_text)

    def next_page(self):
        try:
            if self.current_page == 1:
                self.button = self.driver.find_element(By.XPATH, "/html/body/table[3]/tbody/tr/td[2]/a")
                self.button.click()
                self.current_page += 1
                return False
            else:
                self.button = self.driver.find_element(By.XPATH, "/html/body/table[3]/tbody/tr/td[2]/a[2]")
                self.button.click()
                self.current_page += 1
                return False
        except NoSuchElementException:
            raise NoSuchElementException

crawler = Crawler()
while True:
    try:
        crawler.scrape_course_list()
        crawler.export_course_list()
        crawler.next_page()
    except NoSuchElementException:
        print("done")
        break

crawler.driver.close()
f.close()