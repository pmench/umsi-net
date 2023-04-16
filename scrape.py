import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType, OSType, os_name

import helper as utl


def main():
    """
    Entry point for program.

    :parameter: none.
    :return: none.
    """
    # Configure selenium webdriver for Brave Browser
    # from https://github.com/SergeyPirogov/webdriver_manager/issues/368
    # https://stackoverflow.com/questions/69970256/use-selenium-with-brave-browser-pass-service-object-written-in-python
    binary_location = {
        OSType.LINUX: "/usr/bin/brave-browser",
        OSType.MAC: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        OSType.WIN: f"{os.getenv('LOCALAPPDATA')}\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
    }[os_name()]
    option = webdriver.ChromeOptions()
    option.binary_location = binary_location
    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install(), options=option)

    # Access webpage links for all UMSI faculty
    try:
        urls = utl.read_json('cache.json')["umsi_pages"]
    except FileNotFoundError:
        driver.get('https://www.si.umich.edu/people/directory/faculty')
        nav_elements = driver.find_element(By.CLASS_NAME, 'pager')
        pages = nav_elements.find_elements(By.TAG_NAME, 'li')

        driver.find_element(By.CLASS_NAME, 'directory-teaser-group')
        links = [page.find_elements(By.TAG_NAME, 'a') for page in pages]
        urls = []
        for a_tag in links:
            for element in a_tag:
                if element.get_attribute('href') not in urls:
                    urls.append(element.get_attribute('href'))
        urls = [''.join(list(obj)) for obj in urls]
        utl.save_cache('cache.json', urls, key='umsi_pages')

    # NOTE: UMSI seemed to block all attempts at automating with a loop, including when using with
    # time.sleep() and Selenium Waits
    # Faculty list was created with the below code by manually passing in the index for each url in urls
    # and caching the results
    umsi_faculty = []
    driver.get(urls[10])
    directory_elements = driver.find_element(By.CLASS_NAME, 'directory-teaser-group')
    faculty_elements = directory_elements.find_elements(By.CLASS_NAME, 'research-person-profile')

    people = [element.find_element(By.TAG_NAME, 'h2') for element in faculty_elements]
    names = [person.find_element(By.TAG_NAME, 'a') for person in people]

    umsi_faculty.extend(name.get_attribute('title').replace("'s profile", '') for name in names)
    utl.update_cache('cache.json', umsi_faculty, key='umsi_faculty')

    driver.quit()


if __name__ == '__main__':
    main()
