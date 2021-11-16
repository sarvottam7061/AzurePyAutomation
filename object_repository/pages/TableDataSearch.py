from selenium.webdriver.common.by import By
from PyAuto.PyAutoSelenium import PyAutoWeb


class TableDataSearch(PyAutoWeb):
    locatorTableNav = [(By.PARTIAL_LINK_TEXT, "Table")]
    locatorTableDataSearchSubMenu = [(By.LINK_TEXT, "Table Data Search")]
    locatorClosePopupBtnLink = [(By.LINK_TEXT, "No, thanks!")]
    locatorTaskTable = [(By.ID, "task-table")]
    locatorNotClickable = [(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div/table/thead/tr/th[2]/input")]

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
        self.click_wait_locator(self.locatorTableNav)
        self.click_wait_locator(self.locatorTableDataSearchSubMenu)
        self.wait(2)
        return self

    def element_not_clickable(self):
        self.wait_element_clickable(self.locatorNotClickable)
        self.wait(3)
        return self

    def tables_cell_contains(self, table, row, column, value):
        self.table_cell_should_contain(table, row, column, value)
        return self

    def table_column_contains(self, table_no, col_name, value):
        self.table_column_should_contain(table_no, col_name, value)
        return self

    def table_header_contains(self, table_no, value):
        self.table_header_should_contain(table_no, value)
        return self

    def table_row_contains(self, table_no, row, value):
        self.table_row_should_contain(table_no, row, value)
        return self

    def table_contains(self, table_no, value):
        self.table_should_contain(table_no, value)
        return self

    def get_text_from_table(self):
        self.get_element_text(self.locatorTaskTable)
        return self

    def get_title_of_page(self):
        self.get_title()
        return self
