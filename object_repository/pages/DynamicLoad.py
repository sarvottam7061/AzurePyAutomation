from selenium.webdriver.common.by import By

from PyAuto.PyAutoSelenium import PyAutoWeb
from .AppInputForm import InputForm
from PyAuto.PyAutoLogger import get_logger

logger = get_logger()  # logger to log in allure reports


class DynamicLoad(PyAutoWeb):

    # Define all the locators here. Multiple locator strategy is used,
    # if any one locator fails, framework will take up next in the list
    locatorOthersNav = [(By.PARTIAL_LINK_TEXT, "Others")]
    locatorDynamicMenu = [(By.LINK_TEXT, "Dynamic Data Loading")]
    locatorGetNewBtn = [(By.ID, "sae")]
    locatorFirstNameLbl = [(By.XPATH, "//div[@id='loading']/text()[1]")]
    locatorLastNameLbl = [(By.XPATH, "//div[@id='loading']/text()[2]")]
    locatorLoader = [(By.XPATH, "//img[@src='http://seleniumeasy.com/test/img/loader-image.gif']")]
    locatorUserNameText = [(By.XPATH, "//div[@id='loading']")]

    def __init__(self, driver, url=""):
        super().__init__(driver)  # call super class constructor
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
        self.click_wait_locator(self.locatorOthersNav)
        self.click_wait_locator(self.locatorDynamicMenu)
        self.wait(2)
        return self

    def get_new_user(self):
        self.click_wait_locator(self.locatorGetNewBtn)
        return self

    def wait_user_detail(self):
        self.wait_element_invisible(self.locatorLoader, wait_time=15)
        return self

    def get_values(self):
        # first_name = self.find_element_from_list_wait(self.locatorFirstNameLbl).text
        # self.wait(4)
        name = self.wait_for_name_change()
        logger.error(name)
        names = name.replace("\n", "", 1).split("\n")
        first_name = names[0]
        last_name = names[1]
        first_name_list = first_name.split(" : ")
        last_name_list = last_name.split(" : ")
        values = {}
        values.update({first_name_list[0]: [first_name_list[1]]})
        values.update({last_name_list[0]: [last_name_list[1]]})
        return values

    def wait_for_name_change(self):
        name = self.find_element_from_list_wait(self.locatorUserNameText, wait_time=10).text
        while "First" not in name:
            self.wait(5)
            name = self.find_element_from_list_wait(self.locatorUserNameText, wait_time=10).text
        return name
