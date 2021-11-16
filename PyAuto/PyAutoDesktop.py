import datetime
import os
import time
from pywinauto.controls.win32_controls import ComboBoxWrapper, ButtonWrapper
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from PyAuto.PyAutoException import PyAutoExceptions
from PyAuto.PyAutoLogger import get_logger
from selenium.webdriver.support import expected_conditions as EC

from config import TestConfig as config

screenshot_folder_path = config.screenshot_folder

logger = get_logger()


class PyAutoWindows():

    def __init__(self, app):
        self.app = app

    def take_screenshot(self, screenshot_name=None, screenshot_folder=screenshot_folder_path):
        """
        Take screenshot and save the test with user input name. If no name is provided, test name will be fetched

            Args:
                screenshot_name: pass the name to save or it will fetch the test name for pytest by default. if you
                                 are not using pytest, the name will be screenshot + date time
                screenshot_folder: path to save screenshot in, defaults to screenshot folder in pyautomation framework,
                                   if using pyauto package, the default value is None and should be overridden if not the
                                   screenshot file to be in saved in same folder as execution

            Returns: object of the inherited page class to facilitate method chaining

        """
        if screenshot_name is None:
            try:
                screenshot_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
                print(screenshot_name)
            except:
                screenshot_name = "screenshot"

        if config.desktop_engine == "winappdriver":
            self.sleep(2)
            self.app.save_screenshot(
                screenshot_folder + screenshot_name + datetime.datetime.now().strftime('%Y%m%d_%H-%M-%S') + ".png")
            return self

        if config.desktop_engine == "pywinauto":
            img = self.app.capture_as_image()
            img.save(screenshot_folder + screenshot_name + datetime.datetime.now().strftime('%Y%m%d_%H-%M-%S') + ".png")
            return self

    def find_element_wait(self, locator, wait_for="visible", timeout=10, interval=0.2):
        """
        Find element after waiting for given condition.

            Args:
                locator: locator of type dictionary to locate app element.
                            Ex: locator = {"auto_id": "8047", "title": "New:", "class_name": "Button"}
                wait_for: for winappdriver wait_for could be:
                          'visible' means that the element is visible
                          'presence' means that the element is present
                          'clickable' means that the element is clickable
                          for pywinauto wait_for could be:
                          'exists' means that the window is a valid handle
                          'visible' means that the window is not hidden
                          'enabled' means that the window is not disabled
                          'ready' means that the window is visible and enabled
                          'active' means that the window is active
                timeout: maximum time to search for element.
                interval:time interval for repeated search of element until timeout.

            Returns: returns element

        """
        try:
            if config.desktop_engine == "winappdriver":
                if "auto_id" in locator or "accessibility_id" in locator:
                    locator_value = locator.get("auto_id", None) if locator.get("auto_id", None) else locator.get(
                        "accessibility_id", None)
                    locator_type = "accessibility id"

                elif "title" in locator or "name" in locator:
                    locator_value = locator.get("title", None) if locator.get("title", None) else locator.get(
                        "name", None)
                    locator_type = "name"
                elif "class_name" in locator:
                    locator_value = locator.get("class_name", None)
                    locator_type = "class name"
                elif "id" in locator:
                    locator_value = locator.get("id", None)
                    locator_type = "id"
                elif "tag_name" in locator:
                    locator_value = locator.get("tag_name", None)
                    locator_type = "tag name"
                elif "xpath" in locator:
                    locator_value = locator.get("xpath", None)
                    locator_type = "xpath"

                if wait_for == "visible":
                    web_element = WebDriverWait(self.app, timeout, interval).until(
                        EC.visibility_of_element_located((locator_type, locator_value)),
                        message='Timeout in finding the element')
                elif wait_for == "presence":
                    web_element = WebDriverWait(self.app, timeout, interval).until(
                        EC.presence_of_element_located((locator_type, locator_value)),
                        message='Timeout in finding the element')
                elif wait_for == "clickable" or wait_for == "enabled":
                    web_element = WebDriverWait(self.app, timeout, interval).until(
                        EC.element_to_be_clickable((locator_type, locator_value)),
                        message='Timeout in finding the element')
                return web_element

            if config.desktop_engine == "pywinauto":
                if type(locator) is dict:
                    return self.app.window(**locator).wait(wait_for, timeout, interval)
                elif type(locator) is str:
                    return self.app[locator].wait(wait_for, timeout, interval)
        except:
            raise PyAutoExceptions("Identifying the element failed in " + str(self.__class__.__name__) +
                                   " page, check the error logs for more info")

    def find_elements(self, locator):
        try:
            if config.desktop_engine == "winappdriver":
                if "auto_id" in locator or "accessibility_id" in locator:
                    locator_value = locator.get("auto_id", None) if locator.get("auto_id", None) else locator.get(
                        "accessibility_id", None)
                    return self.wait().app.find_elements_by_accessibility_id(locator_value)
                elif "title" in locator or "name" in locator:
                    locator_value = locator.get("title", None) if locator.get("title", None) else locator.get("name",
                                                                                                              None)
                    return self.wait().app.find_elements_by_name(locator_value)
                elif "class_name" in locator:
                    locator_value = locator.get("class_name", None)
                    return self.wait().app.find_elements_by_class_name(locator_value)
                elif "id" in locator:
                    locator_value = locator.get("id", None)
                    return self.wait().app.find_elements_by_id(locator_value)
                elif "tag_name" in locator:
                    locator_value = locator.get("tag_name", None)
                    return self.wait().app.find_elements_by_tag_name(locator_value)
                elif "xpath" in locator:
                    locator_value = locator.get("xpath", None)
                    return self.wait().app.find_elements_by_xpath(locator_value)

            if config.desktop_engine == "pywinauto":
                if type(locator) is dict:
                    return self.app.find_elements(**locator)
                # else:
                #     return self.app[locator]
        except:
            raise PyAutoExceptions("Identifying the element failed in " + str(self.__class__.__name__) +
                                   " page, check the error logs for more info")

    def wait_element_enabled(self, locator, timeout=10):
        """
        wait till the element got enabled and returns the element.

            Args:
                locator: locator of type dictionary to the element. Ex: locator = {"auto_id" : "4894"}
                timeout: maximum time to search for element.

            Returns: returns element

        """
        try:
            if config.desktop_engine == "winappdriver":
                # element = self.find_element_wait(locator)
                return self.find_element_wait(locator, wait_for="clickable")
            if config.desktop_engine == "pywinauto":
                return self.app.child_window(**locator).wait(wait_for="enabled", timeout=timeout)
        except:
            raise PyAutoExceptions("Element is not enabled " + str(self.__class__.__name__) +
                                   " page, check the error logs for more info")

    def sleep(self, sleep_time=3):
        """
        Hard wait in seconds

            Args:
                sleep_time: time to sleep the thread in seconds. defaults to 3 ->
                            can override seconds by passing it

            Returns: object of the inherited page to facilitate method chaining

        """
        time.sleep(sleep_time)
        return self

    def click_wait_locator(self, locator, wait_for="enabled", timeout=10):
        """
        Find an element and click after waiting for the element to be enabled.

            Args:
                locator: locator of type dictionary to locate app element.
                wait_for: 'exists' means that the window is a valid handle
                          'visible' means that the window is not hidden
                          'enabled' means that the window is not disabled
                          'ready' means that the window is visible and enabled
                          'active' means that the window is active
                timeout: maximum time to search for element.

            Returns: object of the inherited page to facilitate method chaining

        """
        if config.desktop_engine == "winappdriver":
            self.find_element_wait(locator, wait_for, timeout).click()
        if config.desktop_engine == "pywinauto":
            self.find_element_wait(locator, wait_for, timeout).click()
        return self

    def wait(self, timeout=10):
        self.app.implicitly_wait(timeout)
        return self

    def wait_enter_text(self, locator, text, wait_for="enabled", timeout=10):
        """
        Find an element and enter text after waiting for the element to be enabled.

            Args:
                locator: locator of type dictionary to locate app element.
                text: text to be entered.
                wait_for: 'exists' means that the window is a valid handle
                          'visible' means that the window is not hidden
                          'enabled' means that the window is not disabled
                          'ready' means that the window is visible and enabled
                          'active' means that the window is active
                timeout: maximum time to search for element.

            Returns: object of the inherited page to facilitate method chaining

        """
        if config.desktop_engine == "winappdriver":
            self.wait().find_element_wait(locator, wait_for, timeout).send_keys(text)
        if config.desktop_engine == "pywinauto":
            self.find_element_wait(locator, wait_for, timeout).type_keys(text, with_spaces=True)
        return self

    def wait_element_visibility(self, locator, timeout=10):
        """
        Find an element and waiting for the element to be visible.

            Args:
                locator: locator of type dictionary to locate app element.
                timeout: maximum time to search for element visibility.

            Returns: returns element

        """
        if config.desktop_engine == "winappdriver":
            try:
                element = self.find_element_wait(locator)
                if element.is_displayed():
                    return element
            except:
                raise PyAutoExceptions("Identifying the element for visibility failed")

        if config.desktop_engine == "pywinauto":
            return self.find_element_wait(locator, "visible", timeout)

    def element_text_should_be(self, locator, expected_text):
        """
        It will Assert True if the expected_text is EQUAL to element text.

            Args:
                locator: locator of type dictionary to locate app element.
                expected_text: the expected text of the element.

            Returns: returns TRUE or FALSE.

        """
        if config.desktop_engine == "winappdriver":
            text = self.wait().find_element_wait(locator).text
            if expected_text == text:
                assert True
            else:
                assert False, f'Text does not match, expected: {expected_text} and got: {text[0]}'
        if config.desktop_engine == "pywinauto":
            text = self.app.child_window(**locator).texts()
            if expected_text in text:
                assert True
            else:
                assert False, f'Text does not match, expected: {expected_text} and got: {text[0]}'

    def get_automation_id(self, locator):
        """
        fetch and returns the automation id of element.

            Args:
                locator: locator of type dictionary to locate app element.

            Returns: returns the automation id of element.

        """
        if config.desktop_engine == "winappdriver":
            raise PyAutoExceptions("winappdriver don't support this function: get_automation_id ")
        if config.desktop_engine == "pywinauto":
            return self.app.child_window(**locator).automation_id()

    def clear_all_text(self, locator):
        """
        clear the all text of the element.

            Args:
                locator: locator of type dictionary to locate app element.

            Returns: object of the inherited page to facilitate method chaining

        """
        if config.desktop_engine == "winappdriver":
            self.find_element_wait(locator).clear()
        if config.desktop_engine == "pywinauto":
            self.app.child_window(**locator).type_keys("^a+{BACKSPACE}")
        return self

    def get_list_item_count(self, locator):
        """
        get the count of items in list control element.

            Args:
                locator: locator of type dictionary to locate app element of list control.

            Returns: returns the count of items.

        """
        if config.desktop_engine == "winappdriver":
            elements = self.find_elements(locator)
            return len(elements)
        if config.desktop_engine == "pywinauto":
            return self.app.child_window(**locator).item_count()

    def get_list_items(self, locator):
        """
        fetch the list of items and returns the list.

            Args:
                locator: locator of type dictionary to locate app element of list control.

            Returns: list of items.

        """
        if config.desktop_engine == "winappdriver":
            elements = self.find_elements(locator)
            return elements
        if config.desktop_engine == "pywinauto":
            return self.app.child_window(**locator).get_items()

    def select_dropdown_value(self, locator, value):
        """
        selects the value from dropdown.

            Args:
                locator: locator of type dictionary to locate app element.
                value: the value to select from dropdown.

            Returns: object of the inherited page to facilitate method chaining

        """
        if config.desktop_engine == "winappdriver":
            combobox = self.find_element_wait(locator)
            combobox.click()
            combobox.find_element_by_name(value).click()
        if config.desktop_engine == "pywinauto":
            self.app.child_window(**locator).select(value)
        return self

    def double_click_element(self, locator):
        """
        double click the element.

            Args:
                locator: locator of type dictionary to locate app element.

            Returns: object of the inherited page to facilitate method chaining

        """
        if config.desktop_engine == "winappdriver":
            actions = ActionChains(self.app)
            element = self.find_element_wait(locator)
            actions.move_to_element(element)
            actions.double_click()
            actions.perform()
        if config.desktop_engine == "pywinauto":
            self.app.child_window(**locator).double_click_input()
        return self

    # def switch_window(self, window_title, is_open=True, path=None, timeout=15):
    #     main_app = self.app
    #     if is_open is True:
    #         app2 = Application(backend="uia").connect(title=window_title, timeout=timeout)[window_title]
    #     elif is_open is False:
    #         if path is not None:
    #             app2 = Application(backend="uia").start(path=path).connect(title=window_title, timeout=timeout)[
    #                 window_title]
    #     app2.set_focus()
    #     self.app = app2
    #     return main_app

    def mouse_drag_and_drop_by_offset(self, locator, x_offset, y_offset, src=None, button="left", pressed="",
                                      absolute=True):
        """
        drag and drop the element.

            Args:
                locator: locator of type dictionary to locate app element.
                x_offset: x_offset coordinate.
                y_offset: y_offset coordinate.
                src: source wrapper object or coordinates.. if src is None the self is used as a source object.
                button: is a mouse button to hold during the drag.
                        It can be "left", "right", "middle" or "x"
                pressed: a key on the keyboard to press during the drag.
                absolute: specifies whether to use absolute coordinates
                          for the mouse pointer locations

            Returns: object of the inherited page to facilitate method chaining

        """
        if config.desktop_engine == "winappdriver":
            if src is None:
                src = self.find_element_wait(locator)
            ac = ActionChains(self.app)
            ac.drag_and_drop_by_offset(src, x_offset, y_offset).perform()
        if config.desktop_engine == "pywinauto":
            self.app.child_window(**locator).drag_mouse_input((x_offset, y_offset), src, button, pressed, absolute)
        return self

    def right_click_at_coordinate(self, x_offset, y_offset):
        """
        mouse right click at given coordinates.

            Args:
                x_offset: pixels value to click on x-offset
                y_offset: pixels to click on y-offset

            Returns: object of the inherited page to facilitate method chaining

        """
        if config.desktop_engine == "winappdriver":
            ac = ActionChains(self.app)
            ac.move_by_offset(x_offset, y_offset).context_click().perform()
        if config.desktop_engine == "pywinauto":
            self.app.right_click_input(coords=(x_offset, y_offset))
        return self

    def right_click_at_element(self, locator):
        """
        mouse right click at the given element.

            Args:
                locator: locator of type dictionary to locate app element.

            Returns: object of the inherited page to facilitate method chaining

        """
        if config.desktop_engine == "winappdriver":
            item = self.find_element_wait(locator)
            actions = ActionChains(self.app)
            actions.context_click(item).perform()
        if config.desktop_engine == "pywinauto":
            self.app.child_window(**locator).right_click_input()
        return self

    def is_child_of(self, child_locator, parent_locator=None):
        """
        checks if the given child_locator is child of the given parent_locator and return true.

            Args:
                child_locator: locator of type dictionary to locate child element.
                parent_locator: locator of type dictionary to locate parent element.

            Returns: returns TRUE or FALSE

        """
        if config.desktop_engine == "winappdriver":
            raise PyAutoExceptions("winappdriver don't support this function: is_child_of ")
        if config.desktop_engine == "pywinauto":
            if parent_locator is None:
                return self.find_element_wait(child_locator).is_child(self.app)
            else:
                return self.find_element_wait(child_locator).is_child(self.app.child_window(**parent_locator))

    # ----------------------------------------------------------------------------------------------------------

    def checkbox_should_be_checked(self, checkbox_locator):
        """
        assert that the given checkbox element should be checked.

            Args:
                checkbox_locator: locator of element of type dictionary.

            Returns: object of the inherited page to facilitate method chaining

        """
        if config.desktop_engine == "winappdriver":
            checkbox_status = self.find_element_wait(checkbox_locator)
            assert checkbox_status.is_selected()
            return self
        if config.desktop_engine == "pywinauto":
            checkbox_locator = self.app.child_window(**checkbox_locator)
            checkbox = ButtonWrapper(checkbox_locator)
            if checkbox.is_checked() is True:
                assert True
            else:
                assert False, f'Element: {checkbox_locator} is not checked'

        return self

    def checkbox_should_be_unchecked(self, checkbox_locator):
        """
        assert that the given checkbox element should NOT be checked.

            Args:
                checkbox_locator: locator of type dictionary to locate checkbox control element.

            Returns: object of the inherited page to facilitate method chaining

        """
        if config.desktop_engine == "winappdriver":
            if self.find_element_wait(checkbox_locator).is_selected():
                assert False, f'expected was False but got True'
            else:
                assert True
            return self
        if config.desktop_engine == "pywinauto":
            checkbox_locator = self.app.child_window(**checkbox_locator)
            checkbox = ButtonWrapper(checkbox_locator)
            if checkbox.is_checked() is False:
                assert True
            else:
                assert False, f"Element: {checkbox_locator} is not checked"
            return self

    # def verify_the_window_exists(self, window_name):
    #     """
    #     verify if the given window exist or not.
    #
    #         Args:
    #             window_name: title of the window.
    #
    #
    #         Returns: object of the inherited page to facilitate method chaining
    #
    #     """
    #     if config.desktop_engine == "winappdriver":
    #         raise PyAutoExceptions("winappdriver don't support this function: verify_the_window_exists ")
    #     if config.desktop_engine == "pywinauto":
    #         all_windows = Desktop(backend="uia").windows()
    #         windows_list = [w.window_text() for w in all_windows]
    #         if window_name in windows_list:
    #             assert True
    #         else:
    #             assert False
    #         return self

    def get_element_text(self, locator):
        """
        get the text of given element

            Args:
                locator: locator of element of type dictionary.

            Returns: text of element as list.

        """
        if config.desktop_engine == "winappdriver":
            return self.find_element_wait(locator).text
        if config.desktop_engine == "pywinauto":
            # will return the text as a list
            element = self.app.child_window(**locator)
            try:
                element_text = ComboBoxWrapper(element)
                return element_text.texts()
            except:
                raise Exception("The element was not found")

    def button_should_be_enabled(self, locator):
        """
        assert that the button should be enabled.

            Args:
                locator: locator of element of type dictionary.

            Returns: object of the inherited page to facilitate method chaining

        """
        if config.desktop_engine == "winappdriver":
            assert self.find_element_wait(locator).is_enabled(), f'button is not enabled:{locator}'
            return self
        if config.desktop_engine == "pywinauto":
            try:
                element = self.app.child_window(**locator)
            except:
                raise Exception("Element Not Found")
            if element.is_enabled() is True:
                assert True
            else:
                assert False, f'button is not enabled:{locator}'

            return self

    def button_should_be_disabled(self, locator):
        """
        assert that the button should be disabled.

            Args:
                locator: locator of type dictionary of element.

            Returns: object of the inherited page to facilitate method chaining

        """
        if config.desktop_engine == "winappdriver":
            if self.find_element_wait(locator).is_enabled():
                assert False, f'button is not disabled'
            else:
                assert True
            return self
        if config.desktop_engine == "pywinauto":
            try:
                element = self.app.child_window(**locator)
            except:
                raise Exception("Element Not Found")
            if element.is_enabled() is False:
                assert True
            else:
                assert False, f'button is not disabled'
            return self

    # def wait_until_window_opens(self, current_window, wait_time=5):
    #     """
    #     wait until the window opens
    #
    #         Args:
    #             current_window:
    #             wait_time: maximum time to wait for window to open
    #
    #         Returns: object of the inherited page to facilitate method chaining
    #
    #     """
    #     try:
    #         current_window.wait(wait_for="ready", timeout=15, retry_interval=wait_time)
    #     except:
    #         raise Exception("The window handle is not valid")
    #     return self

    def bring_window_to_foreground(self, app=None, window_handle=None):
        """
        brings the given window to foreground.
            Args:
                app: for pywinauto send child window object.
                window_handle: for winappdriver send window handle

            Returns: object of the inherited page to facilitate method chaining

        """
        if config.desktop_engine == "winappdriver":
            self.app.switch_to().window(window_handle)
            return self
        if config.desktop_engine == "pywinauto":
            try:
                app.set_focus()
            except:
                raise Exception("The window handle is not valid")
            return self

    def element_should_be_visible(self, locator):
        """
        asserts that the given element should be visible.

            Args:
                locator: locator of element of type dictionary.

            Returns: object of the inherited page to facilitate method chaining

        """
        if config.desktop_engine == "winappdriver":
            try:
                element = self.find_element_wait(locator, timeout=5)
                if element.is_displayed():
                    assert True
                else:
                    assert False
            except:
                raise PyAutoExceptions("element is not visible")

        if config.desktop_engine == "pywinauto":
            try:
                element = self.app.child_window(**locator)
                ele = ButtonWrapper(element)
            except:
                raise Exception("The element was not found")

            if ele.is_visible() is True:
                assert True
            else:
                assert False, f"Element: {locator}, is not visible"

            return self

    def get_parent_of_element(self, locator):
        """
        fetch the parent of the given element.

            Args:
                locator: for pywinauto: locator of element of type dictionary.
                         for winappdriver: xpath is required in locator list.

            Returns: parent of the element

        """
        if config.desktop_engine == "winappdriver":
            if "xpath" in locator:
                locator_value = locator.get("xpath", None)
                element = self.wait().app.find_element_by_xpath(locator_value + "/..")
            return element
        if config.desktop_engine == "pywinauto":
            element_parent = self.find_element_wait(locator).parent()
            # print(element.parent())
            return element_parent
