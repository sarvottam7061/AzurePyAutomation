from selenium.webdriver.common.by import By
from PyAuto.PyAutoSelenium import PyAutoWeb
from .AppInputForm import InputForm


class DownloadProgress(PyAutoWeb):

    # Define all the locators here. Multiple locator strategy is used,
    # if any one locator fails, framework will take up next in the list
    locatorProgressBarNav = [(By.PARTIAL_LINK_TEXT, "Progress Bars")]
    locatorJqueryDownloadMenu = [(By.LINK_TEXT, "JQuery Download Progress bars")]
    locatorStartDownloadBtn = [(By.ID, "downloadButton")]
    locatorCancelDownloadBtn = [(By.XPATH, "//button[normalize-space()='Cancel Download']")]
    locatorClosePopButton = [(By.XPATH, "//button[normalize-space()='Close']")]

    def __init__(self, driver, url=""):
        super().__init__(driver)   # call super class constructor
        self.driver = driver
        # if you create an object with url, it will validate the url for current page
        self.url = driver.current_url if url == "" else url
        if driver.current_url != self.url:
            self.driver.get(self.url)

    # methods to perform operation in the page following page object model
    def close_pop(self):
        self.click_wait_locator(InputForm.locatorClosePopupBtnLink)
        return self

    def navigate(self):
        self.close_pop()
        self.click_wait_locator(self.locatorProgressBarNav)
        self.click_wait_locator(self.locatorJqueryDownloadMenu)
        self.wait(2)
        return self

    def start_download(self):
        self.click_wait_locator(self.locatorStartDownloadBtn)
        return self

    def invisible_cancel(self, waitTime):
        self.wait_element_invisible(self.locatorCancelDownloadBtn, wait_time=waitTime)
        return self

    def close_download(self):
        self.click_wait_locator(self.locatorClosePopButton)
        return self
