from selenium.webdriver.common.by import By
from PyAuto.PyAutoSelenium import PyAutoWeb


class AutoWebHome(PyAutoWeb):

    # Define all the locators here. Multiple locator strategy is used,
    # if any one locator fails, framework will take up next in the list
    locatorGetQuote = [(By.ID, "nav_automobile")]
    locatorLinkTruck = [(By.ID, "nav_truck")]
    locatorLinkMotor = [(By.ID, "nav_motorcycle")]
    locatorLinkCamper = [(By.ID, "nav_camper")]
    locatorFooterLinkAbout = [(By.ID, "tricentis_about")]
    locatorFooterLinkProducts = [(By.ID, "tricentis_products")]
    locatorFooterLinkEvents = [(By.ID, "tricentis_events")]
    locatorFooterLinkResources = [(By.ID, "tricentis_resources")]

    def __init__(self, driver, url=""):
        super().__init__(driver)  # call super class constructor
        self.driver = driver
        # if you create an object with url, it will validate the url for current page
        self.url = driver.current_url if url == "" else url
        if driver.current_url != self.url:
            self.driver.get(self.url)

    # methods to perform operation in the page following page object model
    def navigate_insurance(self):
        self.click_wait_locator(self.locatorGetQuote)
        return self

    def navigate_auto(self):
        self.click_wait_locator(self.locatorGetQuote)
        return self

    def navigate_truck(self):
        self.click_wait_locator(self.locatorLinkTruck)
        return self

    def navigate_motor(self):
        self.click_wait_locator(self.locatorLinkMotor)
        return self

    def navigate_Camper(self):
        self.click_wait_locator(self.locatorLinkCamper)
        return self

    def navigate_About(self):
        self.click_wait_locator(self.locatorFooterLinkAbout)
        return self

    def navigate_Products(self):
        self.click_wait_locator(self.locatorFooterLinkProducts)
        return self

    def navigate_Events(self):
        self.click_wait_locator(self.locatorFooterLinkEvents)
        return self

    def navigate_Resources(self):
        self.click_wait_locator(self.locatorFooterLinkResources)
        return self
