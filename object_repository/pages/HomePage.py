from selenium.webdriver.common.by import By
from PyAuto.PyAutoSelenium import PyAutoWeb
from PyAuto.PyAutoReadWrite import ReadWrite


class HomePage(PyAutoWeb):
    locatorListBoxNav = [(By.PARTIAL_LINK_TEXT, "List Box")]
    locatorClosePopupBtnLink = [(By.LINK_TEXT, "No, thanks!")]
    locatorSiteNameLogo = [(By.XPATH, "//*[@id=\"site-name\"]/a")]
    locatorViewAllSeleniumTutorials = [(By.LINK_TEXT, "View All Selenium Tutorials")]
    locatorDroppableElement = [(By.ID, "mydropzone")]

    def __init__(self, driver, url=""):
        super().__init__(driver)  # call super class constructor
        self.driver = driver
        # if you create an object with url, it will validate the url for current page
        self.url = driver.current_url if url == "" else url
        if driver.current_url != self.url:
            self.driver.get(self.url)

    def close_pop(self):
        self.click_wait_locator(self.locatorClosePopupBtnLink)
        self.wait(2)
        return self

    def perform_double_click(self):
        self.close_pop()
        self.double_click_element(self.locatorListBoxNav)
        self.wait(2)
        return self

    def get_all_links_in_page(self):
        self.get_all_links()
        return self

    def get_text_of_sitename(self):
        element = self.find_element_from_list(self.locatorSiteNameLogo)
        self.get_element_text(element)
        return self

    def validate_text_of_sitename_logo(self, expected_string):
        self.close_pop()
        # self.element_text_should_be(self.find_element_from_list(self.locatorSiteNameLogo), expected_string)
        self.element_text_should_be(self.locatorSiteNameLogo, expected_string)
        return self

    def scroll_to_element(self):
        self.close_pop()
        element = self.find_element_from_list(self.locatorViewAllSeleniumTutorials)
        self.scroll_element_into_view(element)
        self.wait(3)
        return self

    def validate_page_should_contain(self, expected_text):
        self.close_pop()
        self.page_should_contain_text(expected_text)
        return self

    def validate_page_should_contain_element(self):
        self.close_pop()
        self.page_should_contain_element(self.locatorSiteNameLogo)
        return self

    def execute_js(self, js_code):
        self.close_pop()
        self.execute_javascript(js_code)
        self.wait(2)
        return self

    def validate_page_should_not_contain_element(self):
        self.close_pop()
        self.page_should_not_contain_element(self.locatorDroppableElement)
        return self
