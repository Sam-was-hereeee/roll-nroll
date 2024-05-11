import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
from lxml import etree
import time

f_in = open("courses_selenium.txt", "rt", encoding='utf-8')
f_out = open("courses_brief.txt", "wt", encoding='utf-8')
all_courses = f_in.readlines()
base_url = "https://nol.ntu.edu.tw/nol/coursesearch/"

for course in all_courses:
    c = course.split('/')
    id = c[0]
    try:
        link = c[6]
    except IndexError:
        print(id, "is not a valid")
        continue
    if link == "no_link":
        f_out.write(id + "no_link\n")
        print(id, "is no link")
    else:
        try:
            response = requests.get(base_url + link)
            tree = etree.HTML(response.text)
            elements = tree.xpath("/html/body/table/tbody/tr[2]/td")
            new_tree = etree.Element(elements[0].tag)
            # Append selected elements to the new tree
            for element in elements:
                new_tree.append(element)

            # Serialize the new tree to string
            new_tree_string = etree.tostring(new_tree, pretty_print=True, method="text", encoding="UTF-8")
            new_tree_string = new_tree_string.decode("utf-8")
            new_tree_string = new_tree_string.replace('\n', '-')
            print(new_tree_string)
            f_out.write(id + new_tree_string + "\n")
        except IndexError as e:
            print("index_error")
            continue

