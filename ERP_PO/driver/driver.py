from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def browser():
    service = Service(executable_path=r"C:\develop\app\AIDevelopTool\envs\PyAutoTest\Scripts\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    return driver