from selenium.webdriver.common.by import By
from PyAuto.PyAutoSelenium import PyAutoWeb


class TwitterLogin(PyAutoWeb):

    # Define all the locators here. Multiple locator strategy is used,
    # if any one locator fails, framework will take up next in the list
    locatorUsernameTxt = [(By.NAME, "session[username_or_email]"),
                          (By.XPATH, "//input[@name='session[username_or_email]']"), ]
    locatorPassTxt = [
        (By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]")]
    locatorSigninButton = [
        (By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div/div')]

    def __init__(self, driver, url=""):
        super().__init__(driver)  # call super class constructor
        self.driver = driver
        # if you create an object with url, it will validate the url for current page
        self.url = driver.current_url if url == "" else url
        if driver.current_url != self.url:
            self.driver.get(self.url)

    # methods to perform operation in the page following page object model
    def login(self, user_name, password):
        self.enter_text(user_name, self.locatorUsernameTxt, waitStrategy="clickable")
        self.enter_text(password, self.locatorPassTxt, waitStrategy="clickable")
        self.click_wait_locator(self.locatorSigninButton)
        return self
