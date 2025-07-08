import time
from selenium.webdriver.common.by import By

from ERP_PO.Website.test_case.model.DataManage import Data
from ERP_PO.Website.test_case.model.function import click_element_by_text, read_csv
from ERP_PO.Website.test_case.page_object.BasePage import Page
from ERP_PO.driver.driver import browser


class AddGoods(Page):
    goods_loc = (By.CSS_SELECTOR, "a[href='/gen/product/manage']")
    newlyAdded_loc = (By.CSS_SELECTOR, "#app > div > div.main-container.hasTagsView > section > div > div.mb8.el-row > div:nth-child(3) > button")
    name_loc = (By.CSS_SELECTOR, "body > div.el-dialog__wrapper > div > div.el-dialog__body > form > div:nth-child(1) > div > div > div > input")
    class_loc = (By.CSS_SELECTOR, "#select_class")
    class_ul_loc = (By.CSS_SELECTOR, "body > div.el-select-dropdown.el-popper.option_class > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul")
    brand_loc = (By.CSS_SELECTOR, "#select_brand")
    # brand_ul_loc = (By.CSS_SELECTOR, "body > div.el-select-dropdown.el-popper.option_class > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul")
    unit_loc = (By.CSS_SELECTOR, "body > div.el-dialog__wrapper > div > div.el-dialog__body > form > div:nth-child(4) > div > div > div > div > input")
    # unit_ul_loc = (By.CSS_SELECTOR, "body > div:nth-child(13) > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul")
    purchase_price_loc = (By.CSS_SELECTOR, "body > div.el-dialog__wrapper > div > div.el-dialog__body > form > div:nth-child(5) > div > div > div > input")
    selling_price_loc = (By.CSS_SELECTOR, "body > div.el-dialog__wrapper > div > div.el-dialog__body > form > div:nth-child(6) > div > div > div > input")
    picture_loc = (By.CSS_SELECTOR, "body > div.el-dialog__wrapper > div > div.el-dialog__body > form > div:nth-child(7) > div > div > div > div > input")
    save_loc = (By.CSS_SELECTOR, "body > div.el-dialog__wrapper > div > div.el-dialog__footer > div > button:nth-child(1)")
    pass_loc = (By.CSS_SELECTOR, ".el-message__content")
    error_loc = (By.CSS_SELECTOR, ".el-form-item__error")

    def type_goods(self):
        self.find_element(self.goods_loc).click()

    def type_newlyAdded(self):
        self.find_element(self.newlyAdded_loc).click()

    def type_name(self,name):
        self.find_element(self.name_loc).clear()
        self.find_element(self.name_loc).send_keys(name)

    def type_class(self,name):
        self.find_element(self.class_loc).click()
        ul = self.find_element(self.class_ul_loc)
        ul.find_element(By.CSS_SELECTOR, rf"li[title='{name}']").click()

    def type_brand(self,name):
        self.find_element(self.brand_loc).click()
        time.sleep(1)
        click_element_by_text(name, offset=(10, 0))
        # ul = self.find_element(self.brand_ul_loc)
        # ul.find_element(By.CSS_SELECTOR, rf"li[title='{name}']").click()

    def type_unit(self,name):
        self.find_element(self.unit_loc).click()
        time.sleep(1)
        click_element_by_text(name, offset=(10, 0))
        # ul = self.find_element(self.unit_ul_loc)
        # ul.find_element(By.CSS_SELECTOR, rf"li[title='{name}']").click()

    def type_purchase(self,price):
        self.find_element(self.purchase_price_loc).clear()
        self.find_element(self.purchase_price_loc).send_keys(price)

    def type_selling(self,price):
        self.find_element(self.selling_price_loc).clear()
        self.find_element(self.selling_price_loc).send_keys(price)

    def type_picture(self,picture):
        self.find_element(self.picture_loc).send_keys(picture)

    def type_save(self):
        self.find_element(self.save_loc).click()

    def get_pass_ts(self):
        return self.find_element(self.pass_loc).text

    def get_error_ts(self):
        return self.find_element(self.error_loc).text



def test_add_goods(driver,name,className,brandName,unitName,purchasePrice,sellingPrice,picture):
    add = AddGoods(driver)
    add.type_goods()
    time.sleep(1)
    add.type_newlyAdded()
    time.sleep(1)
    add.type_name(name)
    add.type_class(className)
    add.type_brand(brandName)
    add.type_unit(unitName)
    add.type_purchase(purchasePrice)
    add.type_selling(sellingPrice)
    add.type_picture(picture)
    time.sleep(1)
    add.type_save()
    time.sleep(1)
