from selenium.webdriver.common.by import By
from PyAuto.PyAutoSelenium import PyAutoWeb


class CheckboxDemo(PyAutoWeb):
    locatorInputFormNav = [(By.PARTIAL_LINK_TEXT, "Input Forms")]
    locatorCheckboxDemoSubMenu = [(By.LINK_TEXT, "Checkbox Demo")]
    locatorClosePopupBtnLink = [(By.LINK_TEXT, "No, thanks!")]
    locatorCheckBox = [(By.ID,"isAgeSelected")]

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

    def click_on_checkbox(self):
        self.click_wait_locator(self.locatorCheckBox)
        return self

    def navigate(self):
        self.close_pop()
        self.click_wait_locator(self.locatorInputFormNav)
        self.click_wait_locator(self.locatorCheckboxDemoSubMenu)
        self.wait(2)
        return self

    def validate_checkbox_selection(self):
        self.checkbox_should_be_selected(self.locatorCheckBox)
        return self

    def validate_checkbox_not_selected(self):
        self.checkbox_should_not_be_selected(self.locatorCheckBox)
        return self

    def perform_double_click_on_checkbox(self):
        self.double_click_element(self.locatorCheckBox)
        self.wait(2)
        return self
