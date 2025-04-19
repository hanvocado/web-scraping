#!/usr/bin/env python
# coding: utf-8

import time
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def scrape_one_page(pageNumber):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    
    driver.get(f"https://awesomeopensource.com/projects/data-visualization?projectPage={pageNumber}")

    list_of_projects = driver.find_elements(By.CLASS_NAME, "aos_project_container")


    time.sleep(3)

    list_of_names = []
    for project in list_of_projects:
        name_element = project.find_element(By.CLASS_NAME, "aos_no_underline")
        name_text = name_element.text
        print(name_text)
        name_words = name_text.split()[:-2]  # Loại bỏ 2 từ cuối
        list_of_names.append(name_words)
        print(name_words)


    time.sleep(3)


    list_of_names = [' '.join(names) for names in list_of_names]

    list_of_links = []
    for x in list_of_projects:
        link_element = x.find_element(By.CLASS_NAME, "aos_no_underline")  # Tìm phần tử chứa link
        link = link_element.get_attribute("href")  # Lấy giá trị href
        list_of_links.append(link)  # Thêm vào danh sách


    time.sleep(3)


    list_of_counts = []
    for x in list_of_projects:
        count_element = x.find_element(By.CLASS_NAME, "aos_project_count")  # Tìm phần tử
        count_text = count_element.text.replace(",", "")  # Xóa dấu phẩy
        count_number = float(count_text)  # Chuyển thành số thực
        list_of_counts.append(count_number)  # Thêm vào danh sách

    time.sleep(3)


    list_of_description = []
    for x in list_of_projects:
        desc_element = x.find_element(By.CLASS_NAME, "aos_project_description")  # Tìm phần tử chứa mô tả
        description = desc_element.text  # Lấy nội dung văn bản
        list_of_description.append(description)  # Thêm vào danh sách


    time.sleep(3)

    time.sleep(5)


    # check number of project
    print(len(list_of_names), len(list_of_counts), 
        len(list_of_links), len(list_of_description))


    import pandas as pd


    # dictionary_projects
    dictionary_projects = {"name": list_of_names, 
                        "counts": list_of_counts, 
                        "url": list_of_links, 
                        'descript': list_of_description}


    df = pd.DataFrame(dictionary_projects)

    df.to_excel(f'projects_{pageNumber}.xlsx')
    print(f'Done page {pageNumber}')
    driver.close()

if __name__ == "__main__":
    num_pages = int(input("How many pages do you want to scrape? "))

    for page in range(1, num_pages + 1):
        scrape_one_page(page)