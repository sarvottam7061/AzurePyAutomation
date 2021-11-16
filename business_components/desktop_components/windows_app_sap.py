import allure
from pywinauto.timings import Timings

from PyAuto.PyAutoLogger import get_logger
from object_repository.screens.Calculator import Calc
from object_repository.screens.HpPosDemo import PosDemo
from object_repository.screens.MainScreenSap import MainScreen
from object_repository.screens.SapGuiAuto import SapGuiPom

logger = get_logger()


@allure.step("wait for next button to be enable")
def wait_new_entry_next_enable(app):
    MainScreen(app).navigate().wait_next_enable()


@allure.step("wait for next to be clicked")
def wait_click_next(app):
    MainScreen(app).navigate().wait_next_click()


@allure.step("enter text for new entry")
def enter_text_new_entry(app, description, app_server, inst_num, sys_id):
    Timings.Fast()
    MainScreen(app).navigate().wait_enter_text_new_entry(description, app_server, inst_num, sys_id)


@allure.step("wait till visibility")
def wait_till_visible(app):
    MainScreen(app).wait_till_application_server_visible()


@allure.step("check the text should be")
def the_text_should_be(app, text):
    MainScreen(app).navigate().check_text_should_be(text)


@allure.step("fetch the automation id")
def get_the_auto_id(app):
    MainScreen(app).navigate().get_auto_id_finish()


@allure.step("clear the description")
def clear_description_entry(app):
    MainScreen(app).navigate().clear_description()


@allure.step("select list view from dropdown and get count and item list")
def select_and_get_items(app):
    MainScreen(app).navigate_to_list_view_dropdown().get_the_list_items()


@allure.step("double click to connect to server")
def click_and_connect(app):
    MainScreen(app).double_click_to_connect()


@allure.step("drag and drop the app window")
def drag_drop_app_window(app):
    MainScreen(app).drag_and_drop_window()


@allure.step("right click at the given coordinated")
def right_click_coordinates(app):
    MainScreen(app).right_click_at_given_coordinate()


@allure.step("right click the given element")
def right_click_given_element(app):
    MainScreen(app).right_click_element()


@allure.step("check if the given element is child is of given parent")
def check_is_child_of(app):
    MainScreen(app).check_child_of()


@allure.step("addition in calc")
def check_add_calc(app):
    Calc(app).addition()


@allure.step("square in calc")
def check_sq_calc(app):
    Calc(app).square()


@allure.step("checkout order credit")
def checkout_order_pos(app, card_num):
    PosDemo(app).checkout_order_credit(card_num)


@allure.step("checkout order cash")
def checkout_order_pos_cash(app):
    PosDemo(app).checkout_order_cash()


@allure.step("take screen shot of app")
def screen_shot_app(app):
    MainScreen(app).screen_shot_sap()


@allure.step("checkbox unchecked")
def checkbox_unchecked(app):
    MainScreen(app).navigate().checkbox_element()


@allure.step("get parent")
def element_should_enable(app):
    MainScreen(app).navigate()


def login_sap_session(session):
    SapGuiPom(
        session).open_connection().login_sap().enter_tcode().create_sales_doc().create_standard_order().display_header_details().get_doc_complete().save_and_get_order_number()
