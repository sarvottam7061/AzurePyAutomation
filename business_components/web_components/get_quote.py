from object_repository.pages.QuoteAutoHome import AutoWebHome
from object_repository.pages.QuoteAuto import AutoWebQuote
from object_repository.pages.AppInputForm import InputForm
import allure


@allure.step("updating the quote details")
def autoquote_home_page_1(driver):
    auto_home = AutoWebHome(driver)
    auto_home.navigate_insurance()
    auto_quote = AutoWebQuote(driver)
    auto_quote.enter_data_for_Quote_Page1()


@allure.step("updating the quote details")
def autoquote_home_page_test_data(driver, make, ep, dom, noOFSeats, fuel_type, lp, license_plate, mileage):
    auto_home = AutoWebHome(driver)
    auto_home.navigate_insurance()
    auto_quote = AutoWebQuote(driver)
    auto_quote.enter_data_for_Quote_Page1(make, ep, dom, noOFSeats, fuel_type, lp, license_plate, mileage)


@allure.step("submit user information")
def input_form_test_data(driver, fname, lname, email, phone, Address, city, state, zip_code, website, hosting,
                         project_desc):
    input_form = InputForm(driver, "https://www.seleniumeasy.com/test/input-form-demo.html")
    input_form.enter_data_and_send(fname, lname, email, phone, Address, city, state, zip_code, website, hosting,
                                   project_desc)


@allure.step("Header link validateion - navigate to truck quote")
def quote_navigate_truck(driver):
    auto_home = AutoWebHome(driver)
    auto_home.navigate_truck()
    assert driver.current_url == "http://sampleap.tricentis.com/101/app.php", "url does not match"


@allure.step("Header link validateion - navigate to motor bike quote")
def quote_navigate_motor(driver):
    auto_home = AutoWebHome(driver)
    auto_home.navigate_motor()
    assert driver.current_url == "http://sampleapp.tricentis.com/101/app.php", "url does not match"


@allure.step("Header link validateion - navigate to camper quote")
def quote_navigate_camper(driver):
    auto_home = AutoWebHome(driver)
    auto_home.navigate_Camper()
    assert driver.current_url == "http://sampleapp.tricentis.com/101/app.php", "url does not match"


@allure.step("Header link validation - navigate to auto home quote page")
def quote_navigate_Auto(driver):
    auto_home = AutoWebHome(driver)
    auto_home.navigate_auto()
    assert driver.current_url == "http://sampleapp.tricentis.com/101/app.php", "url does not match"


@allure.step("Footer link validation - navigate to about page")
def footer_navigate_about(driver):
    auto_home = AutoWebHome(driver)
    auto_home.navigate_About()
    assert driver.current_url == "https://www.tricentis.com/company/", "url does not match"


@allure.step("Footer link validation - navigate to products page")
def footer_navigate_products(driver):
    auto_home = AutoWebHome(driver)
    auto_home.navigate_Products()
    assert driver.current_url == "https://www.tricentis.com/tricentis-tosca-testsuite", "url does not match"


@allure.step("Footer link validation - navigate to events page")
def footer_navigate_events(driver):
    auto_home = AutoWebHome(driver)
    auto_home.navigate_Events()
    assert driver.current_url == "https://www.tricentis.com/events/", "url does not match"


@allure.step("Footer link validation - navigate to resources page")
def footer_navigate_resources(driver):
    auto_home = AutoWebHome(driver)
    auto_home.navigate_Resources()
    assert driver.current_url == "https://www.tricentis.com/resources/", "url does not match"
