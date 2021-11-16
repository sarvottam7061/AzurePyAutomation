from selenium import webdriver
from seleniumpagefactory.Pagefactory import PageFactory
import time
from config import TestConfig as config


class InsurantData(PageFactory):

    def __init__(self, driver):
        self.driver = driver  # Required
        self.timeout = config.waitTime  # (Optional - Customise your explicit wait for every webElement)
        # self.highlight = True           #(Optional - To highlight every webElement in PageClass)

    #In page factory all this locator string will be converted into object attributes
    locators = {
        "firstnameTxt": ('ID', 'firstname'),
        "lastnameTxt": ('ID', 'lastname'),
        "dateOfBirthTxt": ('ID', 'birthdate'),
        "maleRadioBtn": ('ID', 'gendermale'),
        "femaleRadioBtn": ('ID', 'genderfemale'),
        "streetAddress": ('XPATH', '//input[@id="streetaddress"]'),
    }

    def enter_insurant_data(self):
        # set_text(), click_button() methods are extended methods in PageFactory
        self.firstnameTxt.set_text("Tester")
        self.lastnameTxt.set_text("Tester2")
        # self.dateOfBirthTxt.set_text("03/12/1992")

    def enter_insurant_data_2(self):
        # set_text(), click_button() methods are extended methods in PageFactory
        self.firstnameTxt.set_text("Wild")
        self.lastnameTxt.set_text("Warrior")
        # self.dateOfBirthTxt.set_text("03/12/1992")
