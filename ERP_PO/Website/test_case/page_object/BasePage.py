class Page():
    def __init__(self,driver):
        self.driver = driver
        self.base_url = "http://192.168.46.5:49460/"

    def _open(self,url):
        url_ = self.base_url + url
        self.driver.get(url_)

    def open(self):
        return self._open(self.url)

    def find_element(self,loc):
        return self.driver.find_element(*loc)