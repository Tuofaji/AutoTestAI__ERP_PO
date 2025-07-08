import ddt
import os
from ERP_PO.Website.test_case.model.function import read_csv, screenshot
from ERP_PO.Website.test_case.model.myunit import StartEnd
from ERP_PO.Website.test_case.page_object.AddBrandPage import test_add_brand, AddBrand
from ERP_PO.Website.test_case.page_object.AddClassPage import test_add_class, AddClass
from ERP_PO.Website.test_case.page_object.AddGoodsPage import test_add_goods, AddGoods
from ERP_PO.Website.test_case.page_object.AddUnitPage import test_add_unit, AddUnit
from ERP_PO.Website.test_case.page_object.LoginPage import test_login
from ERP_PO.Website.test_case.model.DataManage import Data

# Get credentials from environment variables or use defaults for development
DEFAULT_USERNAME = "XTGLY"  # Default for development only
DEFAULT_PASSWORD = "123456"  # Default for development only
TEST_USERNAME = os.environ.get('TEST_USERNAME', DEFAULT_USERNAME)
TEST_PASSWORD = os.environ.get('TEST_PASSWORD', DEFAULT_PASSWORD)


@ddt.ddt
class Test(StartEnd):
    @ddt.data((TEST_USERNAME, TEST_PASSWORD))
    def test01(self, list):
        data = read_csv(Data.BRAND_DATA, 1)
        test_login(self.driver, list[0], list[1])
        test_add_brand(self.driver, data[0])
        screenshot(self.driver, "test_brand.png")
        pass_msg = AddBrand(self.driver).get_pass_ts()
        self.assertIn(pass_msg, data[1])

    @ddt.data((TEST_USERNAME, TEST_PASSWORD))
    def test02(self, list):
        data = read_csv(Data.UNIT_DATA, 1)
        test_login(self.driver, list[0], list[1])
        test_add_unit(self.driver, data[0])
        screenshot(self.driver, "test_unit.png")
        pass_msg = AddUnit(self.driver).get_pass_ts()
        self.assertIn(pass_msg, data[1])

    @ddt.data((TEST_USERNAME, TEST_PASSWORD))
    def test03(self, list):
        data = read_csv(Data.CLASS_DATA, 1)
        test_login(self.driver, list[0], list[1])
        test_add_class(self.driver, data[0])
        screenshot(self.driver, "test_calss.png")
        pass_msg = AddClass(self.driver).get_pass_ts()
        self.assertIn(pass_msg, data[1])

    @ddt.data((TEST_USERNAME, TEST_PASSWORD))
    def test04(self, list):
        data = read_csv(Data.GOODS_DATA, 1)
        test_login(self.driver, list[0], list[1])
        test_add_goods(self.driver, data[0], data[1], data[2], data[3], data[4], data[5], data[6])
        screenshot(self.driver, "test_goods.png")
        pass_msg = AddGoods(self.driver).get_pass_ts()
        self.assertIn(pass_msg, data[7])


