from selenium.webdriver.common.by import By
from PyAuto.PyAutoSelenium import PyAutoWeb


class BootstrapDatePicker(PyAutoWeb):
    # Define all the locators here. Multiple locator strategy is used,
    # if any one locator fails, framework will take up next in the list
    locatorClosePopupBtnLink = [(By.LINK_TEXT, "No, thanks!")]
    locatorDatePicker = [(By.XPATH, "//*[@id='navbar-brand-centered']/ul[1]/li[2]/a")]
    locatorBootstrapDatePicker = [(By.XPATH, "//*[@id='navbar-brand-centered']/ul[1]/li[2]/ul/li[1]/a")]
    locatorCalendar = [(By.XPATH, "//*[@id='sandbox-container1']/div/span")]
    locatorClickCoordinate = [(By.XPATH, "/html/body/div[3]/div[1]/table/tbody/tr[3]/td[4]")]
    locatorPrevious = [(By.XPATH, "/html/body/div[3]/div[1]/table/thead/tr[2]/th[1]")]

    def __init__(self, driver, url=""):
        super().__init__(driver)  # call super class constructor
        self.driver = driver
        # if you create an object with url, it will validate the url for current page
        self.url = driver.current_url if url == "" else url
        if driver.current_url != self.url:
            self.driver.get(self.url)

    # methods to perform operation in the page following page object model

    def open_calendar(self):
        self.click_wait_locator(self.locatorCalendar)
        self.click_wait_locator(self.locatorPrevious)
        self.wait(3)
        return self

    def click_at_coordinate(self, x, y):
        self.click_element_at_coordinate(self.locatorClickCoordinate, x, y)
        self.wait(3)
        return self

    def close_pop(self):
        self.click_wait_locator(self.locatorClosePopupBtnLink)
        return self

    def navigate(self):
        self.close_pop()
        self.click_wait_locator(self.locatorDatePicker)
        self.click_wait_locator(self.locatorBootstrapDatePicker)
        self.wait(2)
        return self
