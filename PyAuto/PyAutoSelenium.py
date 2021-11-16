import pandas as pd
from PIL import Image
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PyAuto.PyAutoLogger import get_logger
from PyAuto.PyAutoHeal import update_page_element, heal_element, get_last_healed_xpath
import os
import datetime
from PyAuto.PyAutoException import handle_selenium_exception, PyAutoExceptions
import time
from selenium.webdriver.support.select import Select
import allure
import requests
import pytest

try:
    from config import TestConfig as config

    screenshot_folder_path = config.screenshot_folder
    explicit_wait_time = config.explicit_wait
    poll_frequency_time = config.poll_time
except:
    screenshot_folder_path = None
    explicit_wait_time = 5
    poll_frequency_time = 0.2

logger = get_logger()

js_style = """
var proto = Element.prototype;
var slice = Function.call.bind(Array.prototype.slice);
var matches = Function.call.bind(proto.matchesSelector || 
                proto.mozMatchesSelector || proto.webkitMatchesSelector ||
                proto.msMatchesSelector || proto.oMatchesSelector);

// Returns true if a DOM Element matches a cssRule
var elementMatchCSSRule = function(element, cssRule) {
  return matches(element, cssRule.selectorText);
};

// Returns true if a property is defined in a cssRule
var propertyInCSSRule = function(prop, cssRule) {
  return prop in cssRule.style && cssRule.style[prop] !== "";
};
const styleSheets = Array.from(document.styleSheets).filter(
      (styleSheet) => !styleSheet.href || styleSheet.href.startsWith(window.location.origin)
    );
// Here we get the cssRules across all the stylesheets in one array
var cssRules = slice(styleSheets).reduce(function(rules, styleSheet) {
  return rules.concat(slice(styleSheet.cssRules));
}, []);
var getAppliedCss = function(elm) {
// get only the css rules that matches that element
var elementRules = cssRules.filter(elementMatchCSSRule.bind(null, elm));
var rules =[];
if(elementRules.length) {
for(i = 0; i < elementRules.length; i++) {
var e = elementRules[i];
rules.push({
    order:i,
    text:e.cssText
})
}
}
if(elm.getAttribute('style')) {
rules.push({
    order:elementRules.length,
    text:elm.getAttribute('style')
})
}
return rules;
}

var rules = getAppliedCss(arguments[0]);

return rules

"""


class PyAutoWeb():

    def __init__(self, driver):
        self.driver = driver

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
            except:
                screenshot_name = "screenshot"
        if screenshot_folder is None:
            self.driver.save_screenshot(
                screenshot_name + datetime.datetime.now().strftime('%Y%m%d_%H-%M-%S') + ".png")
        else:
            self.driver.save_screenshot(
                screenshot_folder + screenshot_name + datetime.datetime.now().strftime('%Y%m%d_%H-%M-%S') + ".png")
        return self

    def find_element_from_list_wait(self, locatorList, waitStrategy="visibility", wait_time=explicit_wait_time,
                                    poll_time=poll_frequency_time):
        """
        Find element after waiting based on the condition

            Args:
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list
                waitStrategy: defaults to visibility, but can be changed to presence or clickable
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                poll_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                           can be overridden by passing values

            Returns: web_element identified or throws, PyAutoException if not found

        """
        web_element = None
        for locator in locatorList:
            try:
                if waitStrategy == "visibility":
                    web_element = WebDriverWait(self.driver, wait_time, poll_time).until(
                        EC.visibility_of_element_located(locator),
                        message='Timeout in finding the element')
                elif waitStrategy == "presence":
                    web_element = WebDriverWait(self.driver, wait_time, poll_time).until(
                        EC.presence_of_element_located(locator),
                        message='Timeout in finding the element')
                elif waitStrategy == "clickable":
                    web_element = WebDriverWait(self.driver, wait_time, poll_time).until(
                        EC.element_to_be_clickable(locator),
                        message='Timeout in finding the element')
                break
            except Exception as E:
                handle_selenium_exception(E, locator)
                continue
        if web_element:
            if config.run_mode == 'capture' or config.run_mode == 'capture&heal':
                html_element = web_element.get_attribute('outerHTML')
                co_ordinates = str(web_element.rect)
                window_size = str(self.driver.get_window_size())
                css_styles = str(self.driver.execute_script(js_style, web_element))
                update_page_element(self, locatorList, html_element, co_ordinates, window_size, css_styles)
        if web_element is None:
            if config.use_last_healed:
                last_healed_xpath = get_last_healed_xpath(self, locatorList)
                if last_healed_xpath:
                    try:
                        web_element = self.driver.find_element_by_xpath(last_healed_xpath[0])
                    except:
                        logger.info(f"Did not have a value for last healed xpath for element in page {str(self.__class__.__name__)}")
            if web_element is None:
                if config.run_mode == 'heal' or config.run_mode=='capture&heal':
                    web_element = heal_element(self, locatorList, self.driver.page_source)
                    if web_element is None:
                        raise PyAutoExceptions("Identifying the element failed in " + str(self.__class__.__name__) +
                                               " page, check the error logs for more info")
                    else:
                        return web_element
                else:
                    raise PyAutoExceptions("Identifying the element failed in " + str(self.__class__.__name__) +
                                           " page, check the error logs for more info")
        return web_element

    def find_element_from_list(self, locatorList):
        """
        Find element from a list of locators without wait

            Args:
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list

            Returns: web_element identified or throws, PyAutoException if not found

        """
        web_element = None
        for locator in locatorList:
            try:
                web_element = self.driver.find_element(*locator)
                break
            except Exception as E:
                handle_selenium_exception(E, locator)
                # e = sys.exc_info()
                # logging.error(str(locator) + str((e[0]).__name__) + ": " + str(e[1]))
                continue
        if web_element is None:
            raise PyAutoExceptions("Identifying the web element failed in " + str(self.__class__.__name__) +
                                   " page, check the error logs for more info")
        return web_element

    def find_elements_from_list(self, locatorList):
        """
        Find elements from a list of locators without wait

            Args:
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list

            Returns: web_elements identified or throws, PyAutoException if not found

        """
        web_elements = None
        for locator in locatorList:
            try:
                web_elements = self.driver.find_elements(*locator)
                break
            except Exception as E:
                handle_selenium_exception(E, locator)
                # e = sys.exc_info()
                # logging.error(str(locator) + str((e[0]).__name__) + ": " + str(e[1]))
                continue

        if web_elements is None:
            raise PyAutoExceptions("Identifying the web element failed in " + str(
                self.__class__.__name__) + " page, check the error logs for more info")
        return web_elements

    # this function performs click on web element whose locator is passed to it.
    def click_wait_locator(self, locatorList, waitStrategy="clickable", wait_time=explicit_wait_time,
                           poll_time=poll_frequency_time):
        """
        Find an element and click after waiting for the element to be clickable(default waitStrategy)

            Args:
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list
                waitStrategy: defaults to clickable, but can pass visibility and presence
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                poll_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                           can be overridden by passing values

            Returns: object of the inherited page to facilitate method chaining

        """
        element = self.find_element_from_list_wait(locatorList, waitStrategy, wait_time, poll_time)
        element.click()
        return self

    def enter_text(self, text, locatorList, waitStrategy="clickable", wait_time=explicit_wait_time,
                   poll_time=poll_frequency_time):
        """
        Find an element and enter text after waiting for the element to be clickable(default waitStrategy)

            Args:
                text: text to be entered
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list
                waitStrategy: defaults to clickable, but can pass visibility and presence
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                poll_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                           can be overridden by passing values

            Returns: object of the inherited page to facilitate method chaining

        """
        element = self.find_element_from_list_wait(locatorList, waitStrategy, wait_time, poll_time)
        element.send_keys(text)
        return self

    def hover_to(self, locatorList, waitStrategy="visibility", wait_time=explicit_wait_time,
                 poll_time=poll_frequency_time):
        """
        Find an element and hover to the element after waiting for the element to be clickable(default waitStrategy)

            Args:
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list
                waitStrategy: defaults to visibility, but can pass clickable and presence
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                poll_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                           can be overridden by passing values

            Returns: object of the inherited page to facilitate method chaining

        """
        element = self.find_element_from_list_wait(locatorList, waitStrategy, wait_time, poll_time)
        ActionChains(self.driver).move_to_element(element).perform()
        return self

    def wait_switch_to_frame(self, locatorList, wait_time=explicit_wait_time,
                             poll_time=poll_frequency_time):
        """
        Switches to the iframe based on the locator

            Args:
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                poll_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                           can be overridden by passing values

            Returns: object of the inherited page to facilitate method chaining

        """
        for locator in locatorList:
            try:
                WebDriverWait(self.driver, wait_time, poll_time).until(
                    EC.frame_to_be_available_and_switch_to_it(locator))
                break
            except Exception as E:
                handle_selenium_exception(E)
                continue
        return self

    def switch_back_parent(self):
        """
        Switches from inside the iframe to parent frame

            Returns: object of the inherited page to facilitate method chaining

        """
        self.driver.switchTo().defaultContent()
        return self

    def switch_to_window(self, window_handle=None):
        """
        Switches to the newly opened window. If window_handle is passed.

            Args:
                window_handle: defaults to None window handle of the window to which the application has to switch

            Returns: object of the inherited page to facilitate method chaining

        """
        window_handles = self.driver.window_handles
        active_window_before_switch = self.driver.current_window_handle
        if len(window_handles) >= 1 and window_handle:
            self.driver.switch_to_window(window_handle)
        elif len(window_handles) > 1 and window_handle is None:
            self.driver.switch_to_window(window_handles[-1])
        else:
            PyAutoExceptions(
                "The number of window/tab opened is " + str(len(window_handles)) + " and not greater than 1")
        return active_window_before_switch

    def wait_page_title(self, title, wait_time=explicit_wait_time, polling_time=poll_frequency_time):
        """
        Waits until the page title condition is true

            Args:
                title: title of the page
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                polling_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                              can be overridden by passing values

            Returns: object of the inherited page to facilitate method chaining

        """
        WebDriverWait(self.driver, wait_time, polling_time).until(
            EC.title_is(title))
        return self

    def wait_page_title_contains(self, title_text, wait_time=explicit_wait_time, polling_time=poll_frequency_time):
        """
        Waits until the page title contains title_text

            Args:
                title_text: partial title of the page to be validated against
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                       can be overridden by passing values
                polling_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                          can be overridden by passing values

            Returns: object of the inherited page to facilitate method chaining

        """

        WebDriverWait(self.driver, wait_time, polling_time).until(
            EC.title_contains(title_text))
        return self

    def wait_element_visibility(self, locatorList, wait_time=explicit_wait_time, polling_time=poll_frequency_time):
        """
        Waits until the element is visible in the page

            Args:
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list.
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values.
                polling_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                              can be overridden by passing values.

            Returns: object of the inherited page to facilitate method chaining.

        """
        web_element = None
        for locator in locatorList:
            try:
                web_element = WebDriverWait(self.driver, wait_time, polling_time).until(
                    EC.visibility_of_element_located(locator))
                break
            except Exception as E:
                handle_selenium_exception(E, locator)
                continue
        if web_element is None:
            raise PyAutoExceptions("Identifying the element failed in " + str(self.__class__.__name__) +
                                   " page, check the error logs for more info")
        return self

    def wait_text_present_locator(self, locatorList, text, wait_time=explicit_wait_time,
                                  polling_time=poll_frequency_time):
        """
        Waits until the text is present in the element

            Args:
                locatorList: locators list of the element
                text: text to be validated against
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                polling_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                              can be overridden by passing values

            Returns: web element identified after wait

        """
        web_element = None
        for locator in locatorList:
            try:
                web_element = WebDriverWait(self.driver, wait_time, polling_time).until(
                    EC.text_to_be_present_in_element(locator, text))
            except Exception as E:
                handle_selenium_exception(E, locator)
                continue
        if web_element is None:
            raise PyAutoExceptions("Identifying the element failed in " + str(self.__class__.__name__) +
                                   " page, check the error logs for more info")
        return web_element

    def wait_element_invisible(self, locatorList, wait_time=explicit_wait_time, polling_time=poll_frequency_time):
        """
        Waits until the element is invisible

            Args:
                locatorList: locators list of the element
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                       can be overridden by passing values
                polling_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                          can be overridden by passing values

            Returns: object of the inherited page to facilitate method chaining

        """
        web_element = None
        for locator in locatorList:
            try:
                web_element = WebDriverWait(self.driver, wait_time, polling_time).until(
                    EC.invisibility_of_element(locator))
                break
            except Exception as E:
                handle_selenium_exception(E, locator)
                continue
        if web_element is None:
            raise PyAutoExceptions("Identifying the element failed in " + str(self.__class__.__name__) +
                                   " page, check the error logs for more info")
        return self

    def select_element_value(self, locatorList, value, waitStrategy="visibility", wait_time=explicit_wait_time,
                             polling_time=poll_frequency_time):
        """
        Select dropdown based on value

            Args:
                locatorList: locators list of the element
                value: value to select from the dropdown
                waitStrategy: defaults to visibility, but can pass clickable and presence
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                polling_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                              can be overridden by passing values

            Returns: object of the inherited page to facilitate method chaining

        """
        element = self.find_element_from_list_wait(locatorList, waitStrategy, wait_time, polling_time)
        Select(element).select_by_value(value)
        return self

    def select_element_index(self, locatorList, index, waitStrategy="visibility", wait_time=explicit_wait_time,
                             polling_time=poll_frequency_time):
        """
        Select dropdown based on index

            Args:
                locatorList: locators list of the element
                index: index to select from the dropdown
                waitStrategy: defaults to visibility, but can pass clickable and presence
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                polling_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                              can be overridden by passing values

            Returns: object of the inherited page to facilitate method chaining

        """
        element = self.find_element_from_list_wait(locatorList, waitStrategy, wait_time, polling_time)
        Select(element).select_by_index(index)
        return self

    def select_element_visible_text(self, locatorList, visible_text, waitStrategy="visibility",
                                    wait_time=explicit_wait_time, polling_time=poll_frequency_time):
        """
        Select dropdown based on visible text

            Args:
                locatorList: locators list of the element
                visible_text: visible text in the dropdown options
                waitStrategy: defaults to visibility, but can pass clickable and presence
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                polling_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                              can be overridden by passing values

            Returns: object of the inherited page to facilitate method chaining

        """
        element = self.find_element_from_list_wait(locatorList, waitStrategy, wait_time, polling_time)
        Select(element).select_by_visible_text(visible_text)
        return self

    def wait(self, seconds=3):
        """
        Hard wait in seconds

            Args:
                seconds: defaults to 3 -> can override seconds by passing it

            Returns: object of the inherited page to facilitate method chaining

        """
        time.sleep(seconds)
        return self

    def check_broken_links(self):
        """
        Fetch all the links from current page, and check for broken link responses

            Returns: object of the inherited page to facilitate method chaining

        """
        redirect_code_range = range(300, 311)
        success_code_range = range(200, 227)
        url_list = []
        for a in self.driver.find_elements_by_xpath('.//a'):
            url_list.append(a.get_attribute('href'))
        for url in url_list:
            with allure.step(f"validating the url:{url}"):
                response = requests.get(url)
                if int(response.status_code) not in success_code_range and int(
                        response.status_code) not in redirect_code_range:
                    logger.error(f"Broken url detected. Got the status code {response.status_code} for url {url}")
                    pytest.assume(False,
                                  f"Broken url detected. Got the status code {response.status_code} for url {url}")
        return self

    # ------------------------------------------------------------------------------------------------

    def checkbox_should_be_selected(self, locatorList):
        """
        It will assert True only if the checkbox element is selected already

            Args:
                locatorList: locators list of the element

            Returns: object of the inherited page to facilitate method chaining

        """
        checkbox = self.find_element_from_list(locatorList)
        assert checkbox.is_selected()
        return self

    def checkbox_should_not_be_selected(self, locatorList):
        """
        It will assert True only if the checkbox element is NOT selected

            Args:
                locatorList: locators list of the element

            Returns: object of the inherited page to facilitate method chaining

        """
        if self.find_element_from_list(locatorList).is_selected():
            assert False, f'expected was False but got True'
        else:
            assert True
        return self

    def clear_element_text(self, locatorList):
        """
        It will Clear all the text that is already present in the element
            Args:
                locatorList: locators list of the element

            Returns: object of the inherited page to facilitate method chaining

        """
        self.find_element_from_list(locatorList).clear()
        return self

    def get_all_cookies(self):
        """
        It will get all the cookies of the current driver instance

            Returns: returns all the cookies

        """
        all_cookies = self.driver.get_cookies()
        return all_cookies

    def delete_all_cookies(self):
        """
        It will delete all the cookies of the current driver instance

            Returns: object of the inherited page to facilitate method chaining

        """
        self.driver.delete_all_cookies()
        return self

    def double_click_element(self, locatorList):
        """
        It will double click the element

            Args:
                locatorList: locators list of the element

            Returns: object of the inherited page to facilitate method chaining

        """
        element = self.find_element_from_list(locatorList)
        action = ActionChains(self.driver)
        action.double_click(element).perform()
        return self

    def drag_and_drop_element(self, source_locatorList, target_locatorList):
        """
        It will drag the element from the source and drop at target

            Args:
                source_locatorList: Locator list of the element to be dragged
                target_locatorList: locator list of the element on which to be dropped

            Returns: object of the inherited page to facilitate method chaining

        """
        source = self.find_element_from_list(source_locatorList)
        target = self.find_element_from_list(target_locatorList)
        action = ActionChains(self.driver)
        action.drag_and_drop(source, target).perform()
        return self

    def drag_and_drop_by_offset(self, source_locatorList, xOffset, yOffset):
        """
        It will drag the element from the source and drop at target according to the offset

            Args:
                source_locatorList: Locator list of the element to be dragged
                xOffset: pixels value to drag element on x-offset
                yOffset: pixels to drag element on y-offset

            Returns: object of the inherited page to facilitate method chaining

        """
        source = self.find_element_from_list(source_locatorList)
        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(source, xOffset, yOffset).perform()
        return self

    def element_should_be_enabled(self, locatorList):
        """
        It will Validate the element should be ENABLED.

            Args:
                locatorList: locators list of the element

            Returns: object of the inherited page to facilitate method chaining

        """
        assert self.find_element_from_list(locatorList).is_enabled(), f'expected was True but got False'
        return self

    def element_should_be_disabled(self, locatorList):
        """
        It will Validate the element should be DISABLED.

            Args:
                locatorList: locators list of the element

            Returns: object of the inherited page to facilitate method chaining

        """
        if self.find_element_from_list(locatorList).is_enabled():
            assert False, f'expected was False but got True'
        else:
            assert True
        return self

    def get_all_attributes(self, locatorList):
        """
        Will return all the attributes of the element

            Args:
                locatorList: locators list of the element

            Returns: it returns all attributes

        """
        element = self.find_element_from_list(locatorList)
        attributes = self.driver.execute_script('var items = {}; for (index = 0; index < arguments['
                                                '0].attributes.length; ++index) { items[arguments[0].attributes['
                                                'index].name] = arguments[0].attributes[index].value }; return '
                                                'items;', element)
        print(attributes)
        return attributes

    def get_all_links(self):
        """
        It will get all the links present in the webpage

            Returns: returns all the links

        """
        linkLocators = [(By.TAG_NAME, "a")]
        all_links = []
        links = self.find_elements_from_list(linkLocators)
        for lnk in links:
            # get_attribute() to get all href
            if lnk.get_attribute('href') is not None:
                all_links.append(lnk.get_attribute('href'))
        # print(all_links)
        return all_links

    # def get_table_cell_at_position(self,locatorList, x_pos, y_pos):
    #     '''
    #
    #     :param locatorList:
    #     :param x_pos:
    #     :param y_pos:
    #     :return:
    #     '''
    #
    #     table = self.find_element_from_list(locatorList)
    #     # t_row = table.find_elements(By.TAG_NAME, "tr")[x_pos]
    #     t_data = table.find_elements(By.TAG_NAME, "td")
    #
    #     # for row in t_row:
    #     #     t_data = row.find_elements(By.TAG_NAME, "td")
    #     #     print(t_data)
    #
    #     # all_rows = []
    #     # for row in t_row:
    #     #     all_rows.append(row.text)
    #     # print(len(all_rows))
    #     # all_col = []
    #     # for col in t_col:
    #     #     all_col.append(col.text)
    #     # print(len(all_col))
    #
    #     all_values = []
    #     for data in t_data:
    #         all_values.append(data.text)
    #     print(all_values)
    #
    #     # t_row = t_row.split(",")
    #     # # value = t_row[y_pos]
    #     # print(t_row)
    #     return self

    def get_element_text(self, web_element):
        """
        It will get the text of element

            Args:
                web_element: web element object

            Returns: text of the web element

        """
        # element_text = self.find_element_from_list(locatorList).text
        # print(web_element.text)
        # return element_text
        return web_element.text

    def get_title(self):
        """
        It will fetch the title of the page.

            Returns: the title of the page

        """
        title_of_page = self.driver.title
        # print(title_of_page)
        return title_of_page

    def delete_the_cookie(self, cookie_name):
        """
        It will delete a particular cookie of the current driver instance

            Args:
                cookie_name: the cookie name to be deleted

            Returns: object of the inherited page to facilitate method chaining

        """
        self.driver.delete_cookie(cookie_name)
        return self

    def element_attribute_value_should_be(self, web_element, element_attr, expected_element_attr_value):
        """
        Assert the value of the attribute of the element

            Args:
                web_element: web element object
                element_attr: attribute of the element
                expected_element_attr_value: expected attribute value of element

            Returns: object of the inherited page to facilitate method chaining

        """

        if isinstance(web_element, list):
            web_element = self.find_element_from_list(web_element)
        assert web_element.get_attribute(
            element_attr) == expected_element_attr_value, f'Expected attribute value :{expected_element_attr_value}, did not match actual attribute value: {web_element.get_attribute(element_attr)}'

        # if isinstance(web_element, WebElement): assert web_element.get_attribute(element_attr) ==
        # expected_element_attr_value, f'Expected attribute value :{expected_element_attr_value}, did not match
        # actual attribute value: {web_element.get_attribute(element_attr)}' elif isinstance(web_element,
        # list): print(type(web_element)) web_element = self.find_element_from_list(web_element) assert
        # web_element.get_attribute(element_attr) == expected_element_attr_value, f'Expected attribute value :{
        # expected_element_attr_value}, did not match actual attribute value: {web_element.get_attribute(
        # element_attr)}'

        return self

    def goto_previous_page(self):
        """
        Go back to the previous page

            Returns: object of the inherited page to facilitate method chaining

        """
        self.driver.back()
        return self

    def element_text_should_be(self, web_element, expected_string):
        """
        It will Assert True if the expected_string is EQUAL to element text

            Args:
                web_element: the Web element to be asserted with
                expected_string: the expected text of element

            Returns: object of the inherited page to facilitate method chaining

        """
        if isinstance(web_element, list):
            web_element = self.find_element_from_list(web_element)
        assert web_element.text == expected_string, f'the expected text: {expected_string}, does not match actual ' \
                                                    f'element text: {web_element.text} '
        return self

    def element_text_should_not_be(self, web_element, expected_string):
        """
        It will Assert True if the expected_string is NOT EQUAL to element text

            Args:
                web_element: the Web element to be asserted with
                expected_string: the text element should not have

            Returns: object of the inherited page to facilitate method chaining

        """
        if isinstance(web_element, list):
            web_element = self.find_element_from_list(web_element)
        assert web_element.text != expected_string, f'the expected text: {expected_string}, matches the actual ' \
                                                    f'element text: {web_element.text} '
        # assert web_element.text.find(sub_string), f'the {sub_string} is not found in element text {
        # web_element.text.find(sub_string)}'
        return self

    def scroll_element_into_view(self, web_element):
        """
        It will scroll to the element into the view.

            Args:
                web_element: the Web element to be viewed

            Returns: object of the inherited page to facilitate method chaining

        """
        action = ActionChains(self.driver)
        action.move_to_element(web_element).perform()
        return self

    def get_page_source(self):
        """
        It will get the page source in text.

            Returns: returns the page source

        """
        return self.driver.page_source

    def page_should_contain_text(self, expected_text):
        """
        Asserts that if the page contains the expected_text

            Args:
                expected_text: the expected text

            Returns: object of the inherited page to facilitate method chaining

        """
        page_source_text = self.get_page_source()
        assert expected_text in page_source_text, f'the page does not contain the text: {expected_text}'
        logger.warning("Number of times it occurs: " + str(page_source_text.count(expected_text)))
        # print("Number of times it occurs:", page_source_text.count(expected_text))
        return self

    def page_should_not_contain_text(self, expected_text):
        """
        Asserts if the page DOES NOT contains the expected_text

            Args:
                expected_text: the expected text

            Returns: object of the inherited page to facilitate method chaining

        """
        page_source_text = self.get_page_source()
        assert expected_text not in page_source_text, f'The page contains the text: {expected_text}'
        return self

    def page_should_contain_element(self, locatorList):
        """
        Asserts if the page contains the Web Element

            Args:
                locatorList: locators list of the element

            Returns: object of the inherited page to facilitate method chaining

        """
        try:
            self.find_element_from_list(locatorList)
        except:
            assert False, f'The page does not contains the element'
        # assert self.find_element_from_list(locatorList)
        return self

    def page_should_not_contain_element(self, locatorList):
        """
        Asserts if the page DOES NOT contains the Web Element

            Args:
                locatorList: locators list of the element

            Returns: object of the inherited page to facilitate method chaining

        """
        try:
            self.find_element_from_list(locatorList)
            assert False, f'The element is present in the page'
        except:
            assert True
        # assert not self.find_element_from_list(locatorList), f'This web element is present in the page'
        return self

    def execute_javascript(self, javascript_code):
        """
        This will manually inject a JavaScript onto that page. Also will work if you have a .js file [for that use:
        read_js_file() from ReadWrite Class]

            Args:
                javascript_code: the javascript code

            Returns: object of the inherited page to facilitate method chaining

        """
        try:
            self.driver.execute_script(javascript_code)
        except Exception as E:
            handle_selenium_exception(E)
        return self

    def get_window_handles(self):
        """
        It will get the window handle of the new window

            Returns: it returns window handles

        """
        # self.switch_to_window()
        return self.driver.window_handles

    def get_window_title(self, window_handle):
        """
        It will get the title of the current window in use

            Args:
                window_handle: window handle for fetching the page title

            Returns: window title of given window handle

        """
        # window = self.switch_to_window(window_handle=self.get_window_handle())
        # self.switch_to_window()
        # self.get_window_handles()
        current_window = self.driver.current_window_handle
        self.switch_to_window(window_handle)
        window_title = self.driver.title
        # print(self.driver.title)
        self.switch_to_window(current_window)
        print(window_title)
        return window_title

    def get_window_size(self, window_handle):
        """
        It will give the size of the window

            Args:
                window_handle: window handle for fetching it's size

            Returns: it returns with window size.

        """
        # self.switch_to_window()
        # self.get_window_handles()
        # print(self.driver.get_window_size())
        # return self.driver.get_window_size()
        current_window = self.driver.current_window_handle
        self.switch_to_window(window_handle)
        window_size = self.driver.get_window_size()
        self.switch_to_window(current_window)
        print(window_size)
        return window_size

    # def close_window(self, window_handle):
    #     '''
    #
    #     :return:
    #     '''
    #     # self.get_window_handles()
    #     # self.driver.close()
    #
    #     current_window = self.driver.current_window_handle
    #     logging.warning(current_window)
    #     logging.warning(window_handle)
    #     print(current_window)
    #     print(window_handle)
    #     self.switch_to_window(window_handle)
    #     time.sleep(10)
    #     # self.driver.close()
    #     # self.switch_to_window(current_window)
    #
    #     # self.switch_to_window()
    #     # self.driver.close()
    #     return self

    # -------------------------------------------------------------------------------------------------------------

    def element_should_visible(self, locator):
        """
        Asserts the visibility of element

            Args:
                locator: the locator list or web element object whose visibility needs to be asserted

            Returns: object of the inherited page to facilitate method chaining

        """
        try:
            if isinstance(locator, list):
                element = self.find_element_from_list_wait(locator)
                assert element.is_displayed() == True
            elif isinstance(locator, WebElement):
                assert locator.is_displayed() == True
        except:
            raise PyAutoExceptions("Element is not visible" + str(self.__class__.__name__) +
                                   " page, check the error logs for more info")
        return self

    def element_should_not_visible(self, locator):
        """
        Asserts the element should NOT be of element

            Args:
                locator: the locator list or web element object whose invisibility needs to be asserted

            Returns: object of the inherited page to facilitate method chaining

        """
        try:
            if isinstance(locator, list):
                element = self.find_element_from_list_wait(locator, "presence")
                assert element.is_displayed(), f'Element is displayed'
            elif isinstance(locator, WebElement):
                assert locator.is_displayed(), f'Element is displayed'
        except:
            assert True
        return self

    def refresh_page(self):
        """
        To refresh the page

            Returns: object of the inherited page to facilitate method chaining

        """
        self.driver.refresh()
        return self

    def set_browser_implicit_wait(self, waiting_time):
        """
        To wait for certain amount of time while searching for element

            Args:
                waiting_time: amount of time to wait (in seconds)

            Returns: object of the inherited page to facilitate method chaining

        """
        self.driver.implicitly_wait(waiting_time)
        return self

    def press_key(self, element, key_name):
        """
        To press key from keyboard

            Args:
                element: element where key need to be pressed
                key_name: key_name can only be:
                         NULL,CANCEL, HELP, BACKSPACE, BACK_SPACE, TAB, CLEAR, RETURN, ENTER, SHIFT,
                         LEFT_SHIFT = SHIFT, CONTROL, LEFT_CONTROL = CONTROL
                         ALT, LEFT_ALT = ALT, PAUSE, ESCAPE, SPACE, PAGE_UP, PAGE_DOWN, END,
                         HOME, LEFT, ARROW_LEFT = LEFT, UP, ARROW_UP = UP, RIGHT, ARROW_RIGHT = RIGHT, DOWN,
                         ARROW_DOWN = DOWN, INSERT, DELETE, SEMICOLON, EQUALS
                         NUMPAD0, NUMPAD1, NUMPAD2, NUMPAD3, NUMPAD4, NUMPAD5, NUMPAD6, NUMPAD7, NUMPAD8, NUMPAD9,
                         MULTIPLY, ADD, SEPARATOR, SUBTRACT, DECIMAL, DIVIDE
                         F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12 META, COMMAND

            Returns: object of the inherited page to facilitate method chaining

        """
        if key_name == 'NULL':
            element.send_keys(Keys.NULL)
        elif key_name == 'CANCEL':
            element.send_keys(Keys.CANCEL)
        elif key_name == 'HELP':
            element.send_keys(Keys.HELP)
        elif key_name == 'BACKSPACE' or key_name == 'BACK_SPACE':
            element.send_keys(Keys.BACKSPACE)
        elif key_name == 'TAB':
            element.send_keys(Keys.TAB)
        elif key_name == 'CLEAR':
            element.send_keys(Keys.CLEAR)
        elif key_name == 'RETURN':
            element.send_keys(Keys.RETURN)
        elif key_name == 'ENTER':
            element.send_keys(Keys.ENTER)
        elif key_name == 'SHIFT' or key_name == 'LEFT_SHIFT':
            element.send_keys(Keys.SHIFT)
        elif key_name == 'CONTROL' or key_name == 'LEFT_CONTROL':
            element.send_keys(Keys.CONTROL)
        elif key_name == 'ALT' or key_name == 'LEFT_ALT':
            element.send_keys(Keys.ALT)
        elif key_name == 'PAUSE':
            element.send_keys(Keys.PAUSE)
        elif key_name == 'ESCAPE':
            element.send_keys(Keys.ESCAPE)
        elif key_name == 'SPACE':
            element.send_keys(Keys.SPACE)
        elif key_name == 'PAGE_UP':
            element.send_keys(Keys.PAGE_UP)
        elif key_name == 'PAGE_DOWN':
            element.send_keys(Keys.PAGE_DOWN)
        elif key_name == 'END':
            element.send_keys(Keys.END)
        elif key_name == 'HOME':
            element.send_keys(Keys.HOME)
        elif key_name == 'LEFT' or key_name == 'ARROW_LEFT':
            element.send_keys(Keys.LEFT)
        elif key_name == 'UP' or key_name == 'ARROW_UP':
            element.send_keys(Keys.UP)
        elif key_name == 'RIGHT' or key_name == 'ARROW_RIGHT':
            element.send_keys(Keys.RIGHT)
        elif key_name == 'DOWN' or key_name == 'ARROW_DOWN':
            element.send_keys(Keys.DOWN)
        elif key_name == 'INSERT':
            element.send_keys(Keys.INSERT)
        elif key_name == 'DELETE':
            element.send_keys(Keys.DELETE)
        elif key_name == 'SEMICOLON':
            element.send_keys(Keys.SEMICOLON)
        elif key_name == 'EQUALS':
            element.send_keys(Keys.EQUALS)
        elif key_name == 'NUMPAD0':
            element.send_keys(Keys.NUMPAD0)
        elif key_name == 'NUMPAD1':
            element.send_keys(Keys.NUMPAD1)
        elif key_name == 'NUMPAD2':
            element.send_keys(Keys.NUMPAD2)
        elif key_name == 'NUMPAD3':
            element.send_keys(Keys.NUMPAD3)
        elif key_name == 'NUMPAD4':
            element.send_keys(Keys.NUMPAD4)
        elif key_name == 'NUMPAD5':
            element.send_keys(Keys.NUMPAD5)
        elif key_name == 'NUMPAD6':
            element.send_keys(Keys.NUMPAD6)
        elif key_name == 'NUMPAD7':
            element.send_keys(Keys.NUMPAD7)
        elif key_name == 'NUMPAD8':
            element.send_keys(Keys.NUMPAD8)
        elif key_name == 'NUMPAD9':
            element.send_keys(Keys.NUMPAD9)
        elif key_name == 'MULTIPLY':
            element.send_keys(Keys.MULTIPLY)
        elif key_name == 'ADD':
            element.send_keys(Keys.ADD)
        elif key_name == 'SEPARATOR':
            element.send_keys(Keys.SEPARATOR)
        elif key_name == 'SUBTRACT':
            element.send_keys(Keys.SUBTRACT)
        elif key_name == 'DECIMAL':
            element.send_keys(Keys.DECIMAL)
        elif key_name == 'DIVIDE':
            element.send_keys(Keys.DIVIDE)
        elif key_name == 'F1':
            element.send_keys(Keys.F1)
        elif key_name == 'F2':
            element.send_keys(Keys.F2)
        elif key_name == 'F3':
            element.send_keys(Keys.F3)
        elif key_name == 'F4':
            element.send_keys(Keys.F4)
        elif key_name == 'F5':
            element.send_keys(Keys.F5)
        elif key_name == 'F6':
            element.send_keys(Keys.F6)
        elif key_name == 'F7':
            element.send_keys(Keys.F7)
        elif key_name == 'F8':
            element.send_keys(Keys.F8)
        elif key_name == 'F9':
            element.send_keys(Keys.F9)
        elif key_name == 'F10':
            element.send_keys(Keys.F10)
        elif key_name == 'F11':
            element.send_keys(Keys.F11)
        elif key_name == 'F12':
            element.send_keys(Keys.F12)
        elif key_name == 'META':
            element.send_keys(Keys.META)
        elif key_name == 'COMMAND':
            element.send_keys(Keys.COMMAND)
        else:
            raise PyAutoExceptions(f'key name {key_name} is not correct ')
        return self

    # -------------------------------------------------------------------------------------------------------------

    def alert_should_be_present(self, wait_time=explicit_wait_time,
                                poll_time=poll_frequency_time):
        """
        Verifies that an alert is present and by default, accepts it.

            Args:
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                poll_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                           can be overridden by passing values

            Returns: true if alert is present false if alert is NOT present

        """
        try:
            WebDriverWait(self.driver, wait_time, poll_time).until(
                EC.alert_is_present(),
                message='Timeout in finding the alert')
            return True
        except:
            return False

    def alert_should_not_be_present(self, wait_time=explicit_wait_time,
                                    poll_time=poll_frequency_time):
        """
        Verifies that an alert is NOT present

            Args:
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                poll_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                           can be overridden by passing values

            Returns: true if alert is NOT present false if alert present

        """
        try:
            WebDriverWait(self.driver, wait_time, poll_time).until(
                EC.alert_is_present(),
                message='Timeout in finding the alert')
            return False
        except:
            return True

    # def capture_element_screen_shot(self, element, screenshot_name=None, screenshot_folder=screenshot_folder_path):
    #     """
    #     Captures a screenshot of element passed as web element.
    #
    # Args: element: element to capture screenshot. screenshot_name: pass the name to save or it will fetch the test
    # name for pytest by default. if you are not using pytest, the name will be screenshot + date time
    # screenshot_folder: path to save screenshot in, defaults to screenshot folder in pyautomation framework,
    # if using pyauto package, the default value is None and should be overridden if not the screenshot file to be in
    # saved in same folder as execution
    #
    #         Returns: object of the inherited page to facilitate method chaining
    #
    #     """
    #     location = element.location
    #     size = element.size
    #     if screenshot_name is None:
    #         screenshot_name = "screenshot"
    #     if screenshot_folder is None:
    #         self.driver.save_screenshot(
    #             screenshot_name + ".png")
    #     else:
    #         self.driver.save_screenshot(
    #             screenshot_folder + screenshot_name + ".png")
    #
    #     x = location['x']
    #     y = location['y']
    #     width = location['x'] + size['width']
    #     height = location['y'] + size['height']
    #
    #     im = Image.open(screenshot_folder + screenshot_name + ".png")
    #     im = im.crop((x, y, width, height))
    #     im.save(screenshot_folder + screenshot_name + ".png")
    #     return self

    def click_element_at_coordinate(self, locator, x_offset, y_offset):
        """
        The Cursor is moved and the center of the element and x/y coordinates are calculated from that point.

            Args:
                locator: locators list to element
                x_offset: pixels value to click on x-offset
                y_offset: pixels to click on y-offset

            Returns: object of the inherited page to facilitate method chaining

        """
        el = self.find_element_from_list_wait(locator)
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(el, x_offset, y_offset).click().perform()
        return self

    def element_should_be_focused(self, locator):
        """
        Asserts that the element identified by locator is focused.

            Args:
                locator: locators list of element that needs to be checked for focused

            Returns: object of the inherited page to facilitate method chaining

        """
        assert self.find_element_from_list_wait(locator) == self.driver.switch_to.active_element, \
            f'element {locator} is not focused'
        # print(self.find_element_from_list_wait(locator))
        # print(self.driver.switch_to.active_element)
        return self

    # ------------------------------------------------------------------------------------------------------------

    def element_should_contain(self, element, expected_text, ignore_case=False):
        """
        asserts that element should contains expected text.

            Args:
                element: web element
                expected_text: expected text
                ignore_case: ignore the case of text. By default set to False.

            Returns: object of the inherited page to facilitate method chaining

        """
        actual_text = self.get_element_text(element)
        if not ignore_case:
            assert expected_text in actual_text, f'element {element} does Not contain expected text:{expected_text}'
        if ignore_case:
            assert expected_text.lower() in actual_text.lower(), f'element {element} does Not contain expected text:{expected_text}'
        return self

    def element_should_not_contain(self, element, expected_text, ignore_case=False):
        """
        assert that the element should Not contain expected text.

            Args:
                element: web element
                expected_text: expected text
                ignore_case: ignore the case of text. By default set to False.

            Returns: object of the inherited page to facilitate method chaining

        """
        actual_text = self.get_element_text(element)
        if not ignore_case:
            assert expected_text not in actual_text, f'element {element} contains expected text:{expected_text}'
        if ignore_case:
            assert expected_text.lower() not in actual_text.lower(), f'element {element} contains expected text:{expected_text}'
        return self

    def open_context_menu(self, element):
        """
        Opens the context menu on the element.

            Args:
                element: web element

            Returns: object of the inherited page to facilitate method chaining

        """
        action = ActionChains(self.driver)
        action.context_click(element).perform()
        return self

    def read_tables(self, url=None):
        """
        It will help in getting tables from a page or url

            Args:
                url: webpage url can be passed. by default set to None, when url is None it
                     fetch the current page url

            Returns: It returns the list of DataFrame objects.

        """
        if url is None:
            dfs = pd.read_html(self.driver.page_source)
        else:
            dfs = pd.read_html(url)
        return dfs

    def table_cell_should_contain(self, df_no, row, column, expected_text, url=None):
        """
        Asserts that table cell should contain expected text.

            Args:
                df_no: dataframe object number to get the particular table. index starts from Zero.
                row: row number from table
                column: column number from table
                expected_text: text that is expected to be present in particular cell
                url: webpage url can be passed. by default set to None, when url is None it will
                     fetch the current page url

            Returns: object of the inherited page to facilitate method chaining

        """
        dfs = self.read_tables(url)
        df = dfs[df_no]
        assert df.iat[row - 1, column - 1] == expected_text, f'Table cell {row, column}does not contain the expected ' \
                                                             f'text:{expected_text} '
        return self

    def table_column_should_contain(self, df_no, column_name, expected_text, url=None):
        """
        Asserts that table column should contain expected text.

            Args:
                df_no: dataframe number to get the particular table. index starts from Zero.
                column_name: name of column from table
                expected_text: text that is expected to be present in column
                url: webpage url can be passed. by default set to None, when url is None it will
                     fetch the current page url

            Returns: object of the inherited page to facilitate method chaining

        """
        dfs = self.read_tables(url)
        df = dfs[df_no]
        col_list = df[column_name].tolist()
        assert expected_text in col_list, f'Table column: {column_name} does not contain the expected text:{expected_text}'
        return self

    def table_header_should_contain(self, df_no, expected_text, url=None):
        """
        Asserts that table header should contain expected text.

            Args:
                df_no: dataframe number to get the particular table. index starts from Zero.
                expected_text: text that is expected to be present in header
                url: webpage url can be passed. by default set to None, when url is None it
                     fetch the current page url

            Returns: object of the inherited page to facilitate method chaining

        """
        dfs = self.read_tables(url)
        df = dfs[df_no]
        header_list = df.columns.values
        assert expected_text in header_list, f'Table header does not contain the expected text:{expected_text}'
        return self

    def table_row_should_contain(self, df_no, row_num, expected_text, url=None):
        """
        Asserts that table row should contain expected text.

            Args:
                df_no: dataframe number to get the particular table. index starts from Zero.
                row_num: row number from table
                expected_text: text that is expected to be present in row
                url: webpage url can be passed. by default set to None, when url is None it will
                     fetch the current page url

            Returns: object of the inherited page to facilitate method chaining

        """
        dfs = self.read_tables(url)
        df = dfs[df_no]
        header_list = df.iloc[row_num - 1].tolist()
        assert expected_text in header_list, f'Table row: {row_num} does not contain the expected text:{expected_text}'
        return self

    def table_should_contain(self, df_no, expected_text, url=None):
        """
        Asserts that table should contain expected text.

            Args:
                df_no: dataframe number to get the particular table. index starts from Zero.
                expected_text: text that is expected to be present in table.
                url: webpage url can be passed. by default set to None, when url is None it will
                     fetch the current page url

            Returns: object of the inherited page to facilitate method chaining

        """
        dfs = self.read_tables(url)
        df = dfs[df_no]
        assert df.isin([expected_text]).any().any(), f'Table: {df_no} does not contain expected text: {expected_text}'
        return self

    def wait_element_clickable(self, locatorList, wait_time=explicit_wait_time, polling_time=poll_frequency_time):
        """
        Waits until the element is clickable in the page

            Args:
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list.
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values.
                polling_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                              can be overridden by passing values.

            Returns: object of the inherited page to facilitate method chaining.

        """
        web_element = None
        for locator in locatorList:
            try:
                web_element = WebDriverWait(self.driver, wait_time, polling_time).until(
                    EC.element_to_be_clickable(locator))
                break
            except Exception as E:
                handle_selenium_exception(E, locator)
                continue
        if web_element is None:
            raise PyAutoExceptions("Identifying the element failed in " + str(self.__class__.__name__) +
                                   " page, check the error logs for more info")
        return self

    def wait_element_present(self, locatorList, wait_time=explicit_wait_time, polling_time=poll_frequency_time):
        """
        Waits until the element is present in the page

            Args:
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list.
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values.
                polling_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                              can be overridden by passing values.

            Returns: object of the inherited page to facilitate method chaining.

        """
        web_element = None
        for locator in locatorList:
            try:
                web_element = WebDriverWait(self.driver, wait_time, polling_time).until(
                    EC.presence_of_element_located(locator))
                break
            except Exception as E:
                handle_selenium_exception(E, locator)
                continue
        if web_element is None:
            raise PyAutoExceptions("Identifying the element failed in " + str(self.__class__.__name__) +
                                   " page, check the error logs for more info")
        return self
