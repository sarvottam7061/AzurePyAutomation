from selenium.webdriver.common.by import By
from PyAuto.PyAutoSelenium import PyAutoWeb


class OthersPage(PyAutoWeb):
    locatorOthersNav = [(By.PARTIAL_LINK_TEXT, "Others")]
    locatorDragAndDropSubMenu = [(By.LINK_TEXT, "Drag and Drop")]
    locatorClosePopupBtnLink = [(By.LINK_TEXT, "No, thanks!")]
    locatorDraggableElement = [(By.XPATH, "//*[@id=\"todrag\"]/span[2]")]
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
        return self

    def navigate(self):
        self.close_pop()
        self.click_wait_locator(self.locatorOthersNav)
        self.click_wait_locator(self.locatorDragAndDropSubMenu)
        self.wait(2)
        return self

    def drag_element_into_target(self):
        self.drag_and_drop_element(self.locatorDraggableElement, self.locatorDroppableElement)
        self.wait(5)
        return self

    def navigate_to_previous_page(self):
        self.goto_previous_page()
        self.wait(2)
        return self
