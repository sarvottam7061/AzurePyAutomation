from selenium.webdriver.common.by import By
from PyAuto.PyAutoSelenium import PyAutoWeb


class AutoWebQuote(PyAutoWeb):

    # Define all the locators here. Multiple locator strategy is used,
    # if any one locator fails, framework will take up next in the list
    locatorMakeDrp = [(By.ID, "make")]
    locatorModelDrp = [(By.ID, "model")]
    locatorCCText = [(By.ID, "cylindercapacty")]
    locatorEnginePerfText = [(By.ID, "engineperformance")]
    locatorDateOfManText = [(By.ID, "dateofmanufacture")]
    locatorNoOfSeatsDrp = [(By.ID, "numberofseats")]
    locatorListPriceText = [(By.ID, "listprice")]
    locatorAMText = [(By.ID, "annualmileage")]
    locatorNextButton = [(By.ID, "nextenterinsurantdata")]
    locatorFuelDrp = [(By.ID, "fuel")]
    locatorLicensePlateTxt = [(By.ID, "licenseplatenumber")]
    locatorFirstNameText = [(By.ID, "firstname")]
    locatorLastNameText = [(By.ID, "lastname")]
    locatorBirthDateText = [(By.ID, "birthdate")]
    locatorGenderMaleRadio = [(By.ID, "gendermale")]

    def __init__(self, driver, url=""):
        super().__init__(driver)  # call super class constructor
        self.driver = driver
        # if you create an object with url, it will validate the url for current page
        self.url = driver.current_url if url == "" else url
        if driver.current_url != self.url:
            self.driver.get(self.url)

    # methods to perform operation in the page following page object model
    def select_make(self, make):
        self.select_element_value(self.locatorMakeDrp, value=make)
        return self

    def enter_ePerform(self, ePerformance):
        self.enter_text(ePerformance, self.locatorEnginePerfText)
        return self

    def enter_dom(self, dom):
        self.enter_text(dom, self.locatorDateOfManText)
        return self

    def select_nos(self, nos):
        self.select_element_value(self.locatorNoOfSeatsDrp, value=nos)
        return self

    def select_FT(self, fuel_type):
        self.select_element_value(self.locatorFuelDrp, value=fuel_type)
        return self

    def enter_list_price(self, list_price):
        self.enter_text(list_price,  self.locatorListPriceText)
        return self

    def enter_license_plate(self, license_plate):
        self.enter_text(license_plate, self.locatorLicensePlateTxt)
        return self

    def enter_annual_mileage(self, annual_mileage):
        self.enter_text(annual_mileage, self.locatorAMText)
        return self
