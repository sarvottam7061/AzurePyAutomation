from selenium.webdriver.common.by import By
from PyAuto.PyAutoSelenium import PyAutoWeb


class JavascriptAlert(PyAutoWeb):
    locatorClosePopupBtnLink = [(By.LINK_TEXT, "No, thanks!")]
    locatorAlerts = [(By.XPATH, "//*[@id='navbar-brand-centered']/ul[2]/li[2]/a")]
    locatorJavascriptAlert = [(By.XPATH, "//*[@id='navbar-brand-centered']/ul[2]/li[2]/ul/li[5]/a")]
    locatorJsConfirmBox = [(By.XPATH, "//*[@id='easycont']/div/div[2]/div[2]/div[2]/button")]
    locatorElementScreenshot = [(By.XPATH, "//*[@id='easycont']/div/div[2]/div[1]/div[2]")]

    def __init__(self, driver, url=""):
        super().__init__(driver)  # call super class constructor
        self.driver = driver
        # if you create an object with url, it will validate the url for current page
        self.url = driver.current_url if url == "" else url
        if driver.current_url != self.url:
            self.driver.get(self.url)

    # methods to perform operation in the page following page object model
    def confirm_box_js(self):
        self.click_wait_locator(self.locatorJsConfirmBox)
        self.wait(3)
        return self

    def alert_check(self):
        print(self.alert_should_be_present())
        self.wait(3)
        return self

    def no_alert_check(self):
        print(self.alert_should_not_be_present())
        self.wait(3)
        return self

    def take_element_screenshot(self):
        ele = self.find_element_from_list_wait(self.locatorElementScreenshot)
        self.capture_element_screen_shot(ele, "ss1", "C:\\Users\\sonam\\project docs\\")

    def close_pop(self):
        self.click_wait_locator(self.locatorClosePopupBtnLink)
        return self

    def navigate(self):
        self.close_pop()
        self.click_wait_locator(self.locatorAlerts)
        self.click_wait_locator(self.locatorJavascriptAlert)
        self.wait(2)
        return self
