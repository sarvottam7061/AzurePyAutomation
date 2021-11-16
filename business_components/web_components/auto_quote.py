from object_repository.pages.QuoteAuto import AutoWebQuote
import allure


# you can use method chaining or create an object and call function line by line
@allure.step("select make value in make dropdown")
def autoquote_select_make(driver, make):
    auto_quote = AutoWebQuote(driver)
    auto_quote.select_make(make)


@allure.step("enter eperformance in e performance text box")
def autoquote_enter_ePerform(driver, ePerformance):
    auto_quote = AutoWebQuote(driver)
    auto_quote.enter_ePerform(ePerformance)


@allure.step("enter date of manufacture in dom text box")
def autoquote_enter_dom(driver, dom):
    auto_quote = AutoWebQuote(driver)
    auto_quote.enter_dom(dom)


@allure.step("select number of seats in nos dropdown")
def autoquote_select_nos(driver, nos):
    auto_quote = AutoWebQuote(driver)
    auto_quote.select_nos(nos)


@allure.step("select fuel type in fuel type dropdown")
def autoquote_select_FT(driver, fuel_type):
    auto_quote = AutoWebQuote(driver)
    auto_quote.select_FT(fuel_type)


@allure.step("enter list price in list price text box")
def autoquote_enter_list_price(driver, list_price):
    auto_quote = AutoWebQuote(driver)
    auto_quote.enter_list_price(list_price)


@allure.step("enter license plate number in license plate text box")
def autoquote_enter_license_plate(driver, license_plate):
    auto_quote = AutoWebQuote(driver)
    auto_quote.enter_license_plate(license_plate)


@allure.step("enter annual mileage value in annual mileage text box")
def autoquote_enter_annual_mileage(driver, annual_mileage):
    auto_quote = AutoWebQuote(driver)
    auto_quote.enter_annual_mileage(annual_mileage)
