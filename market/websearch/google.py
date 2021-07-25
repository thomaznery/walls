from selenium import webdriver
import time
import re


class WSGoogle:
    def __init__(self, driver) -> None:
        opt = webdriver.ChromeOptions()
        opt.add_argument("--headless")
        opt.add_argument("--disable-gpu")
        opt.add_argument("--disable-xss-auditor")
        opt.add_argument("--disable-web-security")
        opt.add_argument("--disable-extensions")
        opt.add_argument("--allow-running-insecure-content")
        opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-setuid-sandbox")
        opt.add_argument("--disable-webgl")
        opt.add_argument("--disable-popup-blocking")
        ed = webdriver.Chrome(r"chromedriver.exe", options=opt)
        self.driver = ed
        self.url_vix = 'https://www.google.com/search?q=sp500+vix&sxsrf=ALe%5C'

    def get_vix_last(self):
        self.driver.get(self.url_vix)
        div = self.driver.find_element_by_class_name("wGt0Bc")
        div.find_element_by_xpath("//div/span/span/span")
        return re.findall(r'[0-9]{2}[,][0-9]{2}', div.text)[0]

    def quit(self):
        self.driver.quit()
