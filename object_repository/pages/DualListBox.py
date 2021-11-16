from selenium.webdriver.common.by import By
from PyAuto.PyAutoSelenium import PyAutoWeb


class DualListBox(PyAutoWeb):
    locatorListBoxNav = [(By.PARTIAL_LINK_TEXT, "List Box")]
    locatorBootstrapListBoxSubMenu = [(By.LINK_TEXT, "Bootstrap List Box")]
    locatorClosePopupBtnLink = [(By.LINK_TEXT, "No, thanks!")]
    locatorSearchbox = [(By.NAME,"SearchDualList")]

    def __init__(self, driver, url=""):
        super().__init__(driver)  # call super class constructor
        self.driver = driver
        # if you create an object with url, it will validate the url for current page
        self.url = driver.current_url if url == "" else url
        if driver.current_url != self.url:
            self.driver.get(self.url)

    def close_pop(self):
        self.click_wait_locator(self.locatorClosePopupBtnLink)
        return self

    def navigate(self):
        self.close_pop()
        self.click_wait_locator(self.locatorListBoxNav)
        self.click_wait_locator(self.locatorBootstrapListBoxSubMenu)
        self.wait(2)
        return self

    def search_for(self, search_text):
        self.enter_text(search_text, self.locatorSearchbox)
        self.wait(2)
        return self

    def clear_text(self):
        self.clear_element_text(self.locatorSearchbox)
        self.wait(1)
        return self

