from object_repository.pages.SeAlertsAndModals import JavascriptAlert
from object_repository.pages.AppInputForm import InputForm
from object_repository.pages.BootstrapListBox import ListBox
from object_repository.pages.DatePicker import BootstrapDatePicker
from object_repository.pages.DownloadProgress import DownloadProgress
from object_repository.pages.CheckboxDemo import CheckboxDemo
from object_repository.pages.DualListBox import DualListBox
from object_repository.pages.OthersPage import OthersPage
from object_repository.pages.HomePage import HomePage
from object_repository.pages.DynamicLoad import DynamicLoad
from object_repository.pages.WindowPopUpModal import WindowPopupModal
from object_repository.pages.TableDataSearch import TableDataSearch
from PyAuto.PyAutoLogger import get_logger
from PyAuto.PyAutoReadWrite import ReadWrite
from PyAuto.PyAutoSelenium import PyAutoWeb
import pandas as pd
import allure

logger = get_logger()


# Use method chaining by creating an object from the page name
@allure.step("submit user information step 2")
def input_form_test_data_step_2(driver, state, zip_code, website, hosting, project_desc):
    InputForm(driver).select_state(state).enter_zip(zip_code).enter_web(website) \
        .radio_hosting(hosting).enter_desc(project_desc).take_screenshot().click_send()


@allure.step("submit user information step 1")
def input_form_test_data_step_1(driver, fname, lname, email, phone, Address,
                                city):
    InputForm(driver).navigate().enter_fname(fname).enter_lname(lname).enter_email(email).enter_phone(phone) \
        .enter_address(Address).enter_city(city)


@allure.step("Check for broken links in input from page")
def check_for_broken_links_input_form(driver):
    InputForm(driver).navigate().check_broken_links()


@allure.step("start download and wait till completes")
def download_progress(driver):
    DownloadProgress(driver).navigate().start_download().invisible_cancel(15).close_download()


@allure.step("submit user information step 1")
def input_form_test_data_step_1_exception(driver, fname, lname, email, phone, Address,
                                          city):
    InputForm(driver).navigate().enter_fname(fname).enter_lname_except(lname).enter_email(email).enter_phone(phone) \
        .enter_address(Address).enter_city(city)


@allure.step("wait and fetch new user")
def fetch_dynamic_data(driver):
    values = DynamicLoad(driver).navigate().get_new_user().wait_user_detail().get_values()
    return values


@allure.step("write and save it in excel")
def write_values_excel(values):
    df = pd.DataFrame.from_dict(values)
    ReadWrite.write_excel(df, "names.xlsx", "name")


# ----------------------------------------------------------------------------------------------
@allure.step("verify the checkbox should be selected")
def validate_checkbox_selected(driver):
    CheckboxDemo(driver).navigate().click_on_checkbox().validate_checkbox_selection()


@allure.step("verify the checkbox should not be selected")
def validate_checkbox_is_not_selected(driver):
    CheckboxDemo(driver).navigate().validate_checkbox_not_selected()


@allure.step("clear all the text from the element")
def clear_text_from_element(driver, search_item):
    DualListBox(driver).navigate().search_for(search_item).clear_text()


@allure.step("Perform double on a Homepage element")
def perform_double_click(driver):
    CheckboxDemo(driver).navigate().perform_double_click_on_checkbox()
    # HomePage(driver).perform_double_click()


@allure.step("Perform Drag and drop on an Element")
def perform_drag_and_drop_element(driver):
    OthersPage(driver).navigate().drag_element_into_target()


@allure.step("Validate for element ENABLED")
def validate_element_is_enabled(driver, hosting):
    InputForm(driver).navigate().radio_hosting(hosting).validate_element_enabled()


@allure.step("Find all attributes of the element")
def find_all_attributes(driver):
    InputForm(driver).navigate().find_attributes_of_send_button()


@allure.step("Find all the links in the page")
def find_the_links(driver):
    HomePage(driver).close_pop().get_all_links_in_page()


@allure.step("Get the text of the element and title of page")
def get_text_from_the_element(driver):
    HomePage(driver).get_text_of_sitename()


@allure.step("Validate element attribute value")
def validate_element_attribute(driver, attribute, expected_attribute):
    InputForm(driver).navigate().element_attribute_value_validation(attribute, expected_attribute)


@allure.step("Go back to the previous page")
def goto_previous_page(driver):
    OthersPage(driver).navigate().navigate_to_previous_page()


@allure.step("Validate the text present in the element")
def get_text_from_the_element(driver, expected_string):
    HomePage(driver).validate_text_of_sitename_logo(expected_string)


@allure.step("Scroll to the Element")
def scroll_to_element(driver):
    HomePage(driver).scroll_to_element()


@allure.step("Validate page should contain the text")
def page_should_contain_text(driver, expected_text):
    HomePage(driver).validate_page_should_contain(expected_text)


@allure.step("Validate page should contain the element")
def page_should_contain_element(driver):
    HomePage(driver).validate_page_should_contain_element()


@allure.step("Validate page should not contain the element")
def page_should_not_contain_element(driver):
    HomePage(driver).validate_page_should_not_contain_element()


@allure.step("Execute Javascript Code")
def execute_javascript_code(driver, js_code):
    HomePage(driver).execute_js(js_code)


@allure.step("Get Window Name")
def get_window_name(driver):
    WindowPopupModal(driver).navigate().fetch_the_window_title()


@allure.step("Get Window Size")
def get_window_size(driver):
    WindowPopupModal(driver).navigate().fetch_window_size()


# @allure.step("Close Window")
# def close_window(driver):
#     WindowPopupModal(driver).navigate().click_on_fb().close_the_window()

# -----------------------------------------------------------

@allure.step("check visibility of search box")
def is_search_box_visible(driver):
    ListBox(driver).navigate().is_visible()


@allure.step("check non-visibility of search box")
def is_search_box_not_visible(driver):
    ListBox(driver).navigate().is_not_visible()


@allure.step("browser implicit wait")
def wait_for_seconds(driver, time, value):
    ListBox(driver).navigate().search_list(value).set_browser_implicit_wait(time)


@allure.step("dual list box page refresh")
def refresh_list_element(driver, value):
    ListBox(driver).navigate().search_list(value).select_list().move().list_box_page_refresh()


@allure.step("browser implicit wait")
def key_press_backspace(driver, value, key_to_press):
    ListBox(driver).navigate().search_list(value).key_to_press(key_to_press)


@allure.step("alert handling")
def handle_js_alert(driver):
    JavascriptAlert(driver).navigate().confirm_box_js().alert_check()


@allure.step("alert not present")
def handle_js_alert_not_present(driver):
    JavascriptAlert(driver).navigate().confirm_box_js().no_alert_check()


# @allure.step("take screenshot of element")
# def element_screenshot(driver):
#     JavascriptAlert(driver).navigate().take_element_screenshot()


@allure.step("click morbi lea at coordinate")
def click_calendar_date(driver, x, y):
    BootstrapDatePicker(driver).navigate().open_calendar().click_at_coordinate(x, y)


@allure.step("check focused element")
def check_element_should_focused(driver):
    ListBox(driver).navigate().check_focused_element()


# -------------------------------------------------------------------------------------------------------------------

@allure.step("validate element contain text")
def check_element_contains_fas(driver, expected_text):
    ListBox(driver).navigate().element_contains_fas(expected_text)


@allure.step("validate element does Not contain text")
def check_element_not_contain_fas(driver, expected_text):
    ListBox(driver).navigate().element_not_contains_fas(expected_text)


@allure.step("open context menu at search")
def open_menu(driver):
    ListBox(driver).navigate().open_menu_at_search()


@allure.step("get table cell and check for expected text")
def table_contains_loblab_dan(driver, table, row, column, value):
    TableDataSearch(driver).navigate().tables_cell_contains(table, row, column, value)


@allure.step("table column contains the expected text")
def table_column_contains_text(driver, table, column, value):
    TableDataSearch(driver).navigate().table_column_contains(table, column, value)


@allure.step("table header contains the expected text")
def table_header_contains_text(driver, table, value):
    TableDataSearch(driver).navigate().table_header_contains(table, value)


@allure.step("table row contains the expected text")
def table_row_contains_text(driver, table, row, value):
    TableDataSearch(driver).navigate().table_row_contains(table, row, value)


@allure.step("table contains the expected text")
def table_contains_text(driver, table, value):
    TableDataSearch(driver).navigate().table_contains(table, value)


@allure.step("using url table row contains the expected text")
def table_row_contains_text_url(driver, table, row, value, url):
    PyAutoWeb(driver).table_row_should_contain(table, row, value, url)


@allure.step("wait till element is clickable")
def element_is_clickable(driver):
    ListBox(driver).navigate().element_clickable()


@allure.step("wait till not clickable element")
def element_is_not_clickable(driver):
    TableDataSearch(driver).navigate().element_not_clickable()


@allure.step("wait till element is present")
def element_is_present(driver):
    ListBox(driver).navigate().element_present()


@allure.step("wait till element is present(not present)")
def element_is_not_present(driver):
    ListBox(driver).navigate().element_not_present()


@allure.step("get user name after dynamic load")
def get_user_name_load(driver):
    names = DynamicLoad(driver).close_pop().navigate().get_new_user().wait_for_name_change()
    return names

@allure.step("write the name into an excel sheet")
def write_to_excel(names):
    list_names = names.replace("\n", "", 1).split("\n")
    first_name = list_names[0]
    last_name = list_names[1]
    first_name_list = first_name.split(" : ")
    last_name_list = last_name.split(" : ")
    key_values = {first_name_list[0]: [first_name_list[1]], last_name_list[0]:[last_name_list[1]]}
    df = pd.DataFrame.from_dict(key_values)
    ReadWrite.write_excel(df, "names_new.xlsx", "name")

