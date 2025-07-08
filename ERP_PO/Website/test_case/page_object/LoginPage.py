from selenium.webdriver.common.by import By

from ERP_PO.Website.test_case.page_object.BasePage import Page


class Login(Page):
    url = "login?redirect=%2Findex"
    username_loc = (By.CSS_SELECTOR,"#username")
    pwd_loc = (By.CSS_SELECTOR, "#password")
    submit_loc = (By.CSS_SELECTOR, "#signIn")


    def type_username(self,username):
        self.find_element(self.username_loc).clear()
        self.find_element(self.username_loc).send_keys(username)

    def type_pwd(self,pwd):
        self.find_element(self.pwd_loc).clear()
        self.find_element(self.pwd_loc).send_keys(pwd)

    def type_submit(self):
        self.find_element(self.submit_loc).click()


def test_login(driver,username,pwd):
    login = Login(driver)
    login.open()
    login.type_username(username)
    login.type_pwd(pwd)
    login.type_submit()