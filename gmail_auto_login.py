from selenium import webdriver
import time
import undetected_chromedriver as uc 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from getpass import getpass

def find_to_click_recovery_email(driver, b):
    try:
        return driver.find_elements(By, CSS_SELECTOR, b)
    except NoSuchElementException:
        return None
print("Enter your email, password, recovery_email: ")
email, password, recovery_email = "", "", ""
#map(str, input().split())
driver = uc.Chrome(use_subprocess=True)
url = 'https://gmail.com'
driver.get(url)
time.sleep(2)
driver.find_element(By.NAME, 'identifier').send_keys(f'{email}\n')
time.sleep(2)
driver.find_element(By.NAME, 'Passwd').send_keys(f'{password}\n')
time.sleep(2)
b = '#view_container > div > div > div.pwWryf.bxPAYd > div < div.WEQkZc > div > form > span > section > div > div > div > ul > li:nth-child(3) > 3'
"""restore = find_to_click_recovery_email(driver, b)
if restore != None:
    print("Clicked to enter recovery email")
    restore.click()
    time.sleep(2)
    driver.find_element(By.NAME, "knowledgePreregisteredEmailResponse").send_keys(f"{recovery_email}\n") """
print('Done loging email')
input()
driver.quit()