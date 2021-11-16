import sys
import pytest
from config import TestConfig as config

sys.path.append("../../../")
from business_components.web_components.app_selenium_easy import *
import logging

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
from utilities.helper import *
from PyAuto.PyAutoReadWrite import ReadWrite


@pytest.mark.se_input_form
def test_single_send_input_form(driver):
    input_form_test_data_step_1(driver, "test", "test1", "tester03@gmail.com",
                                "7448529709", "Cognizant Test", "Newyork")
    input_form_test_data_step_2(driver, "Washington", "98076", "cognizant.com", "yes", "pytest framework")


@pytest.mark.se_check_broken_link
def test_check_broken_link_input_form(driver):
    check_for_broken_links_input_form(driver)


@pytest.mark.excel_data_driven_se
@pytest.mark.parametrize("fname, lname, email, phone, Address, city, state, zip_code, website, hosting, project_desc",
                         parametrized_test_data_excel_fetch(config.testDataFileName, "TC-01"))
def test_multiple_send_input_form(driver, fname, lname, email, phone, Address, city, state, zip_code, website,
                                  hosting, project_desc):
    input_form_test_data_step_1(driver, fname, lname, email, phone, Address, city)
    input_form_test_data_step_2(driver, state, zip_code, website, hosting, project_desc)


@pytest.mark.wait_and_fetch
def test_multipage_web(driver):
    download_progress(driver)
    values = fetch_dynamic_data(driver)
    assert values is not None
    write_values_excel(values)


@pytest.mark.failed_test
def test_fail_web(driver):
    download_progress(driver)
    assert False


@pytest.mark.failed_test_except
def test_fail_web_exception(driver):
    input_form_test_data_step_1_exception(driver, "test", "test1", "tester03@gmail.com",
                                          "7448529709", "Cognizant Test", "Newyork")


# --------------------------------------------------------------------------------------------

@pytest.mark.validate_checkbox_is_selected
def test_checkbox_validation(driver):
    validate_checkbox_selected(driver)


@pytest.mark.validate_checkbox_is_not_selected
def test_checkbox_validation_is_not_selected(driver):
    validate_checkbox_is_not_selected(driver)


@pytest.mark.clear_text_from_element
def test_clear_all_text_from_element(driver):
    clear_text_from_element(driver, "bootstrap")


@pytest.mark.double_click_element
def test_perform_double_click_on_element(driver):
    perform_double_click(driver)


@pytest.mark.drag_and_drop_an_element
def test_drag_drop_element(driver):
    perform_drag_and_drop_element(driver)


@pytest.mark.validate_the_element_is_enabled
def test_check_element_is_enabled(driver):
    validate_element_is_enabled(driver, "yes")


@pytest.mark.get_the_attributes_of_element
def test_get_all_attributes_of_element(driver):
    find_all_attributes(driver)


@pytest.mark.fetch_all_links
def test_get_all_links(driver):
    find_the_links(driver)


@pytest.mark.get_text_from_element
def test_get_text_from_element(driver):
    get_text_from_the_element(driver)


@pytest.mark.validate_the_element_attribute
def test_validate_element_attribute(driver):
    validate_element_attribute(driver, "name", "hosting")


@pytest.mark.go_to_previous_page
def test_navigate_to_previous_page(driver):
    goto_previous_page(driver)


@pytest.mark.validate_the_text_of_element
def test_validate_text_of_element(driver):
    get_text_from_the_element(driver, "Selenium Easy")


@pytest.mark.scroll_into_element
def test_scroll_element_to_view(driver):
    scroll_to_element(driver)


@pytest.mark.validate_page_should_contain_text
def test_validate_page_contains_text(driver):
    page_should_contain_text(driver, "Selenium")


@pytest.mark.validate_page_should_contain_element
def test_validate_page_contains_element(driver):
    page_should_contain_element(driver)


@pytest.mark.validate_page_should_not_contain_element
def test_validate_page_not_contains_element(driver):
    page_should_not_contain_element(driver)


@pytest.mark.execute_javascript
def test_execute_javascript(driver):
    execute_javascript_code(driver, 'alert("PopUp From JS")')


@pytest.mark.get_window_title
def test_get_window_title(driver):
    get_window_name(driver)


@pytest.mark.fetch_window_size
def test_get_window_size(driver):
    get_window_size(driver)


# @pytest.mark.close_the_window
# def test_close_the_window(driver):
#     close_window(driver)

# ----------------------------------------------------------------------

@pytest.mark.check_search_box_visible
def test_search_box_is_visible(driver):
    is_search_box_visible(driver)


@pytest.mark.check_search_box_not_visible
def test_search_box_is_not_visible(driver):
    is_search_box_not_visible(driver)


@pytest.mark.check_implicit_wait
def test_implicit_wait(driver):
    wait_for_seconds(driver, 5, "Morbi leo risus")


@pytest.mark.check_refresh_page
def test_page_refresh(driver):
    refresh_list_element(driver, "Morbi leo risus")


@pytest.mark.check_backspace_keypress
def test_key_press(driver):
    key_press_backspace(driver, "Morbi leo risus", "BACKSPACE")


@pytest.mark.alert_test
def test_js_alert_should_present(driver):
    handle_js_alert(driver)


@pytest.mark.alert_test_not_present
def test_js_alert_should_not_present(driver):
    handle_js_alert_not_present(driver)


# @pytest.mark.element_screenshot_capture
# def test_element_screenshot(driver):
#     element_screenshot(driver)


@pytest.mark.click_calendar_at_coordinate
def test_click_at_calendar(driver):
    click_calendar_date(driver, 50, 0)


@pytest.mark.check_focused_element
def test_element_is_focused(driver):
    check_element_should_focused(driver)


# ----------------------------------------------------------------------------------------------------------------

@pytest.mark.check_element_should_contain
def test_element_contain_fas(driver):
    check_element_contains_fas(driver, "facilisis")


@pytest.mark.check_element_should_not_contain
def test_element_not_contain_fas(driver):
    check_element_not_contain_fas(driver, "leo")


@pytest.mark.open_menu_context
def test_open_menu_at_search(driver):
    open_menu(driver)


@pytest.mark.check_table_cell_value
def test_table_cell_value(driver):
    table_contains_loblab_dan(driver, 0, 3, 3, "Loblab Dan")


@pytest.mark.check_table_col_value
def test_table_column_value(driver):
    table_column_contains_text(driver, 0, "Assignee", "Holden Charles")


@pytest.mark.check_table_header_value
def test_table_header_value(driver):
    table_header_contains_text(driver, 0, "Assignee")


@pytest.mark.check_table_row_value
def test_table_row_value(driver):
    table_row_contains_text(driver, 1, 4, "Byron")


@pytest.mark.check_table_value
def test_table_value(driver):
    table_contains_text(driver, 0, "Kilgore Trout")


@pytest.mark.check_table_row_value_url
def test_table_row_value_by_url(driver):
    table_row_contains_text_url(driver, 0, 2, "February",
                                "https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_tbody_css")


@pytest.mark.wait_till_element_clickable
def test_element_clickable(driver):
    element_is_clickable(driver)


@pytest.mark.wait_till_element_clickable
def test_element_not_clickable(driver):
    element_is_not_clickable(driver)


@pytest.mark.wait_till_element_present
def test_element_present(driver):
    element_is_present(driver)


@pytest.mark.wait_till_element_present
def test_element_not_present(driver):
    element_is_not_present(driver)



@pytest.mark.dynamic_load
def test_get_name_and_save(driver):
    names = get_user_name_load(driver)
    write_to_excel(names)