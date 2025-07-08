import unittest

from ERP_PO.driver.driver import browser


class StartEnd(unittest.TestCase):
    def setUp(self):
        self.driver = browser()
        self.driver.implicitly_wait(3)
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()