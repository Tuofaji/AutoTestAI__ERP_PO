import time
from selenium.webdriver.common.by import By
from ERP_PO.Website.test_case.page_object.BasePage import Page


class AddClass(Page):
    class_loc = (By.CSS_SELECTOR, "a[href='/gen/product/category']")
    newlyAdded_loc = (By.CSS_SELECTOR, "#app > div > div.main-container.hasTagsView > section > div > div.mb8.el-row > div:nth-child(3) > button")
    input_loc = (By.CSS_SELECTOR, "body > div.el-dialog__wrapper > div > div.el-dialog__body > form > div > div > div > div > input")
    save_loc = (By.CSS_SELECTOR, "body > div.el-dialog__wrapper > div > div.el-dialog__footer > div > button.el-button.el-button--primary.el-button--medium")
    error_loc = (By.CSS_SELECTOR,"body > div.el-dialog__wrapper > div > div.el-dialog__body > form > div > div > div.el-form-item__error")
    pass_loc = (By.CSS_SELECTOR, "body > div.el-message.el-message--success > p")

    def type_class(self):
        self.find_element(self.class_loc).click()

    def type_newlyAdded(self):
        self.find_element(self.newlyAdded_loc).click()

    def type_input(self, name):
        self.find_element(self.input_loc).clear()
        self.find_element(self.input_loc).send_keys(name)

    def type_save(self):
        self.find_element(self.save_loc).click()

    def get_error_ts(self):
        return self.find_element(self.error_loc).text

    def get_pass_ts(self):
        return self.find_element(self.pass_loc).text




def test_add_class(driver, name):
    add = AddClass(driver)
    time.sleep(1)
    add.type_class()
    time.sleep(1)
    add.type_newlyAdded()
    time.sleep(1)
    add.type_input(name)
    time.sleep(1)
    add.type_save()
    time.sleep(1)