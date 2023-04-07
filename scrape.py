import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType, OSType, os_name
from selenium.webdriver.common.by import By


def main():
    """
    Entry point for program.

    :param:
        None
    :return:
        None
    """
    # Configure selenium webdriver
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

    # Access webpages
    driver.get('https://www.si.umich.edu/people/directory/faculty')
    directory_elements = driver.find_element(By.CLASS_NAME, 'directory-teaser-group')
    faculty_elements = directory_elements.find_elements(By.CLASS_NAME, 'research-person-profile')

    people = [element.find_element(By.TAG_NAME, 'h2') for element in faculty_elements]
    names = [person.find_element(By.TAG_NAME, 'a') for person in people]

    for name in names:
        print((name.get_attribute('title').strip('\'s profile')))


if __name__ == '__main__':
    main()
