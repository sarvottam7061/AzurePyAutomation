import pytest

from business_components.desktop_components.windows_app_sap import *

import logging

logger = logging.getLogger()
logger.setLevel(logging.WARNING)


@pytest.mark.wait_next_enable
def test_next_enable_wait(desktop_app):
    wait_new_entry_next_enable(desktop_app)


@pytest.mark.click_wait_next
def test_click_wait_next(desktop_app):
    wait_click_next(desktop_app)


@pytest.mark.enter_new_entry
def test_enter_text(desktop_app):
    enter_text_new_entry(desktop_app, "SAP 7AUTO", "189:23:2:4:2", 67, 234)


@pytest.mark.wait_visibility
def test_wait_till_visibility(desktop_app):
    wait_till_visible(desktop_app)


@pytest.mark.text_should_be_check
def test_the_text_should_be(desktop_app):
    the_text_should_be(desktop_app, "System Connection Parameters")


@pytest.mark.auto_id_fetch
def test_get_the_auto_id_finish(desktop_app):
    get_the_auto_id(desktop_app)


@pytest.mark.clear_all_text
def test_clear_the_entry(desktop_app):
    clear_description_entry(desktop_app)


@pytest.mark.select_and_get
def test_dropdown_select_and_list_item_get(desktop_app):
    select_and_get_items(desktop_app)


@pytest.mark.double_click_connect
def test_double_click_connect(desktop_app):
    click_and_connect(desktop_app)


@pytest.mark.drag_and_drop
def test_drag_and_drop_the_window(desktop_app):
    drag_drop_app_window(desktop_app)


@pytest.mark.right_click_coordinate
def test_right_click_the_coordinate(desktop_app):
    right_click_coordinates(desktop_app)


@pytest.mark.right_click_element
def test_right_click_the_element(desktop_app):
    right_click_given_element(desktop_app)


@pytest.mark.check_is_child_of
def test_check_is_child_of(desktop_app):
    check_is_child_of(desktop_app)


@pytest.mark.calc_addition
def test_calc_add(desktop_app):
    check_add_calc(desktop_app)


@pytest.mark.calc_addition
def test_calc_sq(desktop_app):
    check_sq_calc(desktop_app)


@pytest.mark.hp_pos_demo
def test_checkout_order(desktop_app):
    checkout_order_pos(desktop_app, "1098347739867583")


@pytest.mark.hp_pos_demo
def test_checkout_order_cash(desktop_app):
    checkout_order_pos_cash(desktop_app)


@pytest.mark.test_screen_shot
def test_screen_shot(desktop_app):
    screen_shot_app(desktop_app)


@pytest.mark.test_checkbox
def test_checkbox(desktop_app):
    checkbox_unchecked(desktop_app)


@pytest.mark.get_parent_element
def test_element_parent(desktop_app):
    element_should_enable(desktop_app)


@pytest.mark.sap_login
def test_sap_login(session):
    login_sap_session(session)
