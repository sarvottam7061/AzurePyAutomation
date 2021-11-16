from selenium.webdriver.common.by import By
from PyAuto.PyAutoSelenium import PyAutoWeb


class WindowPopupModal(PyAutoWeb):
    locatorAlertsAndModalsNav = [(By.PARTIAL_LINK_TEXT, "Alerts & Modals")]
    locatorWindowPopupModalSubMenu = [(By.LINK_TEXT, "Window Popup Modal")]
    locatorClosePopupBtnLink = [(By.LINK_TEXT, "No, thanks!")]
    locatorOpenFacebookWindow = [(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div/div[2]/div[2]/a")]

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
        self.click_wait_locator(self.locatorAlertsAndModalsNav)
        self.click_wait_locator(self.locatorWindowPopupModalSubMenu)
        return self

    def fetch_the_window_title(self):
        window_handles = self.get_window_handles()
        self.get_window_title(window_handles[-1])
        return self

    def fetch_window_size(self):
        window_handles = self.get_window_handles()
        self.get_window_size(window_handles[-1])
        return self

    # def close_the_window(self):
    #     self.wait(3)
    #     window_handles = self.get_window_handles()
    #     self.close_window(window_handles[-1])
    #     self.wait(3)
    #     return self

    def click_on_fb(self):
        self.click_wait_locator(self.locatorOpenFacebookWindow)
        self.wait(3)
        return self

