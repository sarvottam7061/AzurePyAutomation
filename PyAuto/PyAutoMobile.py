import textwrap

from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from PyAuto.PyAutoLogger import get_logger
from appium.webdriver.common.touch_action import TouchAction
from PyAuto.PyAutoSelenium import PyAutoWeb

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

from PyAuto.PyAutoException import PyAutoExceptions, handle_selenium_exception


class PyAutoMobile(PyAutoWeb):

    def __init__(self, mob_conn):
        self.mob_conn = mob_conn

    def find_mobile_element_from_list_wait(self, locatorList, waitStrategy="visibility", wait_time=explicit_wait_time,
                                           poll_time=poll_frequency_time):
        '''
        Find element after waiting based on the condition

            Args:
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list
                waitStrategy: defaults to visibility, but can be changed to presence or clickable
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                poll_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                           can be overridden by passing values

            Returns: mobile_element identified or throws Exception if not found
        '''

        mob_element = None
        for locator in locatorList:
            try:
                if waitStrategy == "visibility":
                    mob_element = WebDriverWait(self.mob_conn, wait_time, poll_time).until(
                        EC.visibility_of_element_located(locator),
                        message='Timeout in finding the element')
                elif waitStrategy == "presence":
                    mob_element = WebDriverWait(self.mob_conn, wait_time, poll_time).until(
                        EC.presence_of_element_located(locator),
                        message='Timeout in finding the element')
                elif waitStrategy == "clickable":
                    mob_element = WebDriverWait(self.mob_conn, wait_time, poll_time).until(
                        EC.element_to_be_clickable(locator),
                        message='Timeout in finding the element')
                break
            except:
                PyAutoExceptions("Identifying the element failed.")
                continue
        return mob_element

    def find_mobile_element_and_click(self, locatorList, waitStrategy="clickable", wait_time=explicit_wait_time,
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

        try:
            self.find_mobile_element_from_list_wait(locatorList, waitStrategy, wait_time, poll_time).click()
        except:
            raise PyAutoExceptions(f"Clicking the element failed at locator {locatorList}")
        return self

    def wait_mobile_element_visibility(self, locatorList, wait_time=explicit_wait_time,
                                       polling_time=poll_frequency_time):
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

        mob_element = None
        for locator in locatorList:
            try:
                mob_element = WebDriverWait(self.mob_conn, wait_time, polling_time).until(
                    EC.visibility_of_element_located(locator))
                break
            except Exception:
                raise PyAutoExceptions("Identifying the element failed.")
        if mob_element is None:
            raise PyAutoExceptions("Identifying the element failed.")
        return self

    def get_text_from_mobile_element(self, element):
        """
        Gets the Text from the element

            Args:
                element: Mobile element object

            Returns: The text from the element as a string
        """

        if type(element) is list:
            element = self.find_mobile_element_from_list_wait(element, waitStrategy="visibility")
        return element.text

    def navigate_home_mobile(self):
        """
        Will Navigate to the home screen of the device

            Returns: object of the inherited page to facilitate method chaining.
        """

        if config.desiredCapabilities_mobile['platformName'] == 'android':
            self.mob_conn.press_keycode(187)
        elif config.desiredCapabilities_mobile['platformName'] == 'ios':
            pressHome = {"name": "home"}
            # self.mob_conn.execute_script("mobile: pressButton", pressHome)
            self.mob_conn.execute_script("seetest:client.deviceAction(\"Home\")")
        return self

    def go_back_mobile(self):
        """
        Will go to the previous screen in the mobile device

            Returns: object of the inherited page to facilitate method chaining.
        """

        if config.desiredCapabilities_mobile['platformName'] == 'android':
            self.mob_conn.press_keycode(4)
        elif config.desiredCapabilities_mobile['platformName'] == 'ios':
            self.mob_conn.back()
        return self

    def change_orientation_landscape(self):
        """
        Will change the orientation of the the screen to Landscape-View

            Returns: object of the inherited page to facilitate method chaining.
        """

        self.mob_conn.orientation = 'LANDSCAPE'
        return self

    def change_orientation_portrait(self):
        """
        Will change the orientation of the the screen to Portrait-View

            Returns: object of the inherited page to facilitate method chaining.
        """

        self.mob_conn.orientation = 'PORTRAIT'
        return self

    def open_menu_mobile(self):
        """
        Will open the menu/app_drawer of the device (only for Android)

            Returns: object of the inherited page to facilitate method chaining.
        """

        if config.desiredCapabilities_mobile['platformName'] == 'android':
            self.mob_conn.press_keycode(82)
        # elif config.desiredCapabilities_mobile['platformName'] == 'ios':
        #     pressBack = {"name": "back"}
        #     self.mob_conn.execute_script("mobile: pressButton", pressBack)
        return self

    def touch_and_hold_element(self, element, time_duration=3000):
        """
        Hold the element for a duration of time
            Args:
                element: Element object on which the operation needs to be performed
                time_duration: Number of milli-seconds the element will be hold

            Returns: object of the inherited page to facilitate method chaining
        """

        actions = TouchAction(self.mob_conn)
        actions.long_press(element, duration=time_duration)
        actions.perform()
        return self

    def mobile_swipe_from_direction(self, direction, offset=None, time=1000, element=None):
        """
        Will Swipe to a particular direction from the offset given (Note: Only works with Appium Studio for Android)

            Args:
                element: The element to be swiped
                time: The amount of time in which the operation will be performed
                offset: The offset of the screen
                direction: the direction in which to swipe

            Returns: object of the inherited page to facilitate method chaining.
        """

        if config.desiredCapabilities_mobile['platformName'] == 'android':
            try:
                self.mob_conn.execute_script(f"seetest:client.swipe(\"{direction.capitalize()}\", {offset}, {time})")
            except:
                raise Exception("Swipe Operation is not possible")

        elif config.desiredCapabilities_mobile['platformName'] == 'ios':
            params = {"element": element, "direction": direction}
            self.mob_conn.execute_script("mobile: swipe", params)
        return self

    def swipe_from_coordinates(self, x1, y1, x2, y2, drag_time=1000):
        """
        Swipe on the screen from source-coordinates (x1, y1) to destination-coordinates (x2, y2)

            Args:
                x1: X coordinate of the source on screen
                y1: Y coordinate of the source on screen
                x2: X coordinate of the destination on screen
                y2: Y coordinate of the destination on screen
                drag_time: The amount of time in which the operation will be performed in ms

            Returns: object of the inherited page to facilitate method chaining
        """

        try:
            self.mob_conn.swipe(x1, y1, x2, y2, drag_time)
        except:
            raise Exception("Swipe Operation is not possible")

        return self

    def remove_application(self, appPackage):
        """
        Remove the application from the mobile device

            Args:
                appPackage: appPackage name for android or BundleID for iOS.

            Returns: object of the inherited page to facilitate method chaining
        """

        try:
            self.mob_conn.remove_app(appPackage)
        except:
            raise Exception("Uninstallation is not possible")
        return self

    def open_recent_apps(self):
        """
        Will open background apps section

            Returns: object of the inherited page to facilitate method chaining
        """

        if config.desiredCapabilities_mobile['platformName'] == 'android':
            self.mob_conn.press_keycode(187)
        # elif config.desiredCapabilities_mobile['platformName'] == 'ios':
        #     params = {"element": element, "name": "back"}
        #     self.mob_conn.execute_script("mobile: swipe", params)

    def validate_app_installed(self, appPackage):
        """
        Will validate of the app is installed in the mobile device or not

            Args:
                appPackage: appPackage name for android or BundleID for iOS.

            Returns: object of the inherited page to facilitate method chaining
        """

        assert self.mob_conn.is_app_installed(
            appPackage), f"The Application {appPackage} is not installed in the device."
        return self

    # def get_device_settings(self):
    #     """
    #     Will get the mobile device settings.
    #
    #     Returns:
    #
    #     """
    #     device_settings = self.mob_conn.get_settings()
    #     return device_settings

    def start_new_activity_android(self, appPackage, activityName):
        """
        Will start a new activity on the mobile device

            Args:
                appPackage: appPackage name for android or BundleID for iOS.
                activityName: Activity name that to be launched from the application

            Returns: object of the inherited page to facilitate method chaining
        """

        self.mob_conn.start_activity(appPackage, activityName)
        return self

    def start_new_activity_ios(self, bundleId):
        """
        Will start a new activity on the mobile device

            Args:
                bundleId: The bundle identifier of the application to be launched.

            Returns: object of the inherited page to facilitate method chaining
        """
        params = {"bundleId": bundleId}
        self.mob_conn.execute_script("mobile: launchApp", params)
        return self

    def activate_app_ios(self, bundleId):
        """
        Puts the given application to foreground if it is running in the background. An error is thrown if the app is \
        not installed or is not running

            Args:
                bundleId: The bundle identifier of the application to be launched.

            Returns: object of the inherited page to facilitate method chaining
        """
        try:
            params = {"bundleId": bundleId}
            self.mob_conn.execute_script("mobile: activateApp", params)
        except:
            raise Exception("The App is either not running or not installed")
        return self

    def current_app_info(self):
        """
        Get the appActivity and appPackage of the current running application

            Returns: Returns the application info as a dictionary.
        """

        app_info = {}
        app_activity = self.mob_conn.current_activity
        app_package = self.mob_conn.current_package
        app_info['current_activity'] = app_activity
        app_info['current_package'] = app_package
        return app_info

    def send_app_to_background(self, background_time=100):
        """
        Will send the app to background for a specific amount of time

            Args:
                background_time: How long to run app in background (in seconds)

            Returns: object of the inherited page to facilitate method chaining

        """
        self.mob_conn.background_app(background_time)
        return self

    def close_current_app(self):
        """
        Close an app on device

            Returns: object of the inherited page to facilitate method chaining
        """

        self.mob_conn.close_app()
        return self

    def get_app_status(self, appPackage):
        """
        Get the given app status on the device

            Args:
                appPackage: BundleId for iOS. Package name for Android.

            Returns: State of App in string

        """
        state = self.mob_conn.query_app_state(appPackage)
        if state == 0:
            return "App not installed"
        elif state == 1:
            return "App not running"
        elif state == 2:
            return " App running in background or suspended"
        elif state == 3:
            return "App  running in background"
        elif state == 4:
            return "App running in foreground"

    def enter_text_in_mobile_element(self, text, locatorList, waitStrategy="visibility", wait_time=explicit_wait_time,
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
        element = self.find_mobile_element_from_list_wait(locatorList, waitStrategy, wait_time, poll_time)
        element.send_keys(text)
        return self

    def clear_mobile_element_text(self, locatorList, waitStrategy="clickable", wait_time=explicit_wait_time,
                                  poll_time=poll_frequency_time):
        """
        Clear an element's value

            Args:
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list
                waitStrategy: defaults to clickable, but can pass visibility and presence
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                poll_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                           can be overridden by passing values

            Returns: object of the inherited page to facilitate method chaining
        """

        element = self.find_mobile_element_from_list_wait(locatorList, waitStrategy, wait_time, poll_time)
        element.clear()
        return self

    def check_element_selected_mobile(self, locatorList, waitStrategy="clickable", wait_time=explicit_wait_time,
                                      poll_time=poll_frequency_time):
        """
        Determine if a form or form-like element (checkbox, select, etc...) is selected

            Args:
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list
                waitStrategy: defaults to clickable, but can pass visibility and presence
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                poll_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                           can be overridden by passing values

        Returns: object of the inherited page to facilitate method chaining

        """
        element = self.find_mobile_element_from_list_wait(locatorList, waitStrategy, wait_time, poll_time)
        assert element.is_selected(), f'Expected was true but got false.'
        return self

    def check_element_enabled_mobile(self, locatorList, waitStrategy="clickable", wait_time=explicit_wait_time,
                                     poll_time=poll_frequency_time):
        """
        Determine if an element is currently enabled

            Args:
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list
                waitStrategy: defaults to clickable, but can pass visibility and presence
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                poll_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                           can be overridden by passing values

        Returns: object of the inherited page to facilitate method chaining

        """
        element = self.find_mobile_element_from_list_wait(locatorList, waitStrategy, wait_time, poll_time)
        assert element.is_enabled(), f'Expected was true but got false.'
        return self

    def check_element_displayed_mobile(self, locatorList, waitStrategy="clickable", wait_time=explicit_wait_time,
                                       poll_time=poll_frequency_time):
        """
        Determine if an element is currently displayed

            Args:
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list
                waitStrategy: defaults to clickable, but can pass visibility and presence
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                poll_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                           can be overridden by passing values

        Returns: object of the inherited page to facilitate method chaining
        """

        element = self.find_mobile_element_from_list_wait(locatorList, waitStrategy, wait_time, poll_time)
        assert element.is_displayed(), f'Expected was true but got false.'
        return self

    def get_element_location_mobile(self, locatorList, waitStrategy="clickable", wait_time=explicit_wait_time,
                                    poll_time=poll_frequency_time):
        """
        Determine an element's location on the page or screen in a dictionary format; E.g.: {'x': 568, 'y': 742}

            Args:
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list
                waitStrategy: defaults to clickable, but can pass visibility and presence
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                poll_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                           can be overridden by passing values

            Returns: object of the inherited page to facilitate method chaining
        """

        element = self.find_mobile_element_from_list_wait(locatorList, waitStrategy, wait_time, poll_time)
        element_location = element.location
        return element_location

    def get_element_size_mobile(self, locatorList, waitStrategy="clickable", wait_time=explicit_wait_time,
                                poll_time=poll_frequency_time):
        """
        Determine an element's size in pixels in a dictionary format; E.g.: {'height': 104, 'width': 476}

            Args:
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list
                waitStrategy: defaults to clickable, but can pass visibility and presence
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                poll_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                           can be overridden by passing values

            Returns: object of the inherited page to facilitate method chaining
        """

        element = self.find_mobile_element_from_list_wait(locatorList, waitStrategy, wait_time, poll_time)
        element_size = element.size
        return element_size

    def get_element_location_in_view_mobile(self, locatorList, waitStrategy="clickable", wait_time=explicit_wait_time,
                                            poll_time=poll_frequency_time):
        """
        Determine an element's location on the page or screen in a dictionary format; E.g.: {'x': 568, 'y': 742}

            Args:
                locatorList: list of locators with different strategy to identify the element, can also pass only one inside a list
                waitStrategy: defaults to clickable, but can pass visibility and presence
                wait_time: defaults to explicit wait in test config or if used as pyauto package 5s,
                           can be overridden by passing values
                poll_time: defaults to time mentioned in test config or if used as pyauto package 0.2s,
                           can be overridden by passing values

            Returns: object of the inherited page to facilitate method chaining
        """

        element = self.find_mobile_element_from_list_wait(locatorList, waitStrategy, wait_time, poll_time)
        action = ActionChains(self.mob_conn)
        action.move_to_element(element).perform()
        return self

    def get_current_context(self):
        """
        Get the current context in which Appium is running

            Returns: the current context as a String
        """

        return self.mob_conn.current_context

    def scroll_from_mobile_element(self, origin_el, x_dest, y_dest):
        """
        Scroll from the element on the screen using finger based motion events

        Args:
            origin_el: the element from which to being scrolling
            x_dest: X offset to scroll to
            y_dest: Y offset to scroll to

        Returns: object of the inherited page to facilitate method chaining
        """

        self.mob_conn.scroll_from_element(origin_el, x_dest, y_dest)
        return self

    def flick_mobile_element(self, element, x_coordinate, y_coordinate, speed):
        """
        Flick starting at on_element, and moving by the x and y with specified speed.
            Args:
                speed: Pixels per second to flick.
                element: Flick will start on the element
                x_coordinate: X offset to flick to.
                y_coordinate: Y offset to flick to.

            Returns:

        """
        self.mob_conn.flick_element(element, x_coordinate, y_coordinate, speed)
        return self

    def get_element_attribute(self, locatorList, attribute=None):
        """
        Get the value of an element's attribute

            Args:
                locatorList: Locators to identify the element
                attribute: The attribute of the element

            Returns: value of the attribute or null if not set
        """

        element = self.find_mobile_element_from_list_wait(locatorList)
        tagName = element.get_attribute(attribute)
        return tagName

    def minimize_keyboard(self):
        """
        Hide soft keyboard

            Returns: object of the inherited page to facilitate method chaining
        """

        self.mob_conn.hide_keyboard()
        return self

    def set_context_to(self, set_context):
        """
        Set the context being automated

        Args:
            set_context: The name of the context to which to change

        Returns: object of the inherited page to facilitate method chaining
        """

        self.mob_conn.switch_to.context(set_context)
        return self

    def get_all_contexts(self):
        """
        Get all the contexts available to automate

            Returns: Array of the names of all available contexts

        """
        return self.mob_conn.contexts

    def drag_drop_element(self, source_element, destination_element):
        """
        Drag and drop an element to another element

            Args:
                source_element: Element that has to be dragged
                destination_element: Element where it has to be dropped

            Returns: object of the inherited page to facilitate method chaining

        """
        actions = TouchAction(self.mob_conn)
        actions.long_press(source_element)
        actions.move_to(destination_element)
        actions.release()
        actions.perform()
        return self

    def drag_drop_from_coordinates(self, x1, y1, x2, y2):
        """
        Drag and drop from a source coordinate to destination coordinate

            Args:
                x1: x coordinate of source
                y1: y coordinate of source
                x2: x coordinate of destination
                y2: y coordinate of destination

            Returns: object of the inherited page to facilitate method chaining
        """

        actions = TouchAction(self.mob_conn)
        actions.long_press(x=x1, y=y1)
        actions.move_to(x=x2, y=y2)
        actions.release()
        actions.perform()
        return self

    def retrieve_file_from_device(self, file_path):
        """
        Retrieve a file from the device's file system

            Args:
                file_path: Path on the device to pull file from

            Returns: Contents of file in decoded base64 (string)
        """

        file_base64 = self.mob_conn.pull_file(file_path)
        return file_base64

    def get_text_from_clipboard(self):
        """
        Get the text from Clipboard of the system

            Returns: base64 decoded string
        """

        self.mob_conn.get_clipboard()
        text_from_clipboard = self.mob_conn.get_clipboard_text()
        return text_from_clipboard

    # def decode_from_base64(self, encoded_string):
    #     """
    #     Will Decode a string to ASCII from a base64 encode string
    #         Args:
    #             encoded_string: encoded base64 String
    #
    #     Returns: decoded string in ASCII
    #
    #     """
    #     base64_bytes = encoded_string.encode('ascii')
    #     message_bytes = base64.b64decode(base64_bytes)
    #     decoded_string = message_bytes.decode('ascii')
    #     return decoded_string

    def set_text_to_clipboard(self, text):
        """
        Set the content to the system clipboard

            Args:
                text: The actual clipboard content

            Returns: object of the inherited page to facilitate method chaining
        """
        try:
            self.mob_conn.set_clipboard(text)
        except:
            self.mob_conn.set_clipboard_text(text)
        return self

    def location_service_toggle(self):
        """
        Switch the state of the location service

            Returns: object of the inherited page to facilitate method chaining
        """

        self.mob_conn.toggle_location_services()
        return self

    def send_sms_to_number(self, phone_number, text_message):
        """
        Simulate an SMS message (Emulator only)

            Args:
                phone_number: The phone number to send the SMS to
                text_message: The SMS message

            Returns: object of the inherited page to facilitate method chaining
        """

        self.mob_conn.send_sms(phone_number, text_message)
        return self

    def get_session_capabilities(self):
        """
        Retrieve the capabilities of the specified session

            Returns: An object describing the session's capabilities
        """

        return self.mob_conn.session

    def execute_driver_script(self, script, timeout_for_script=5000):
        """
        Run a WebdriverIO script against the current session.

            Args:
                script: The WebdriverIO script to execute
                timeout_for_script: The number of ms Appium should wait for the script to finish before killing it due to timeout

            Returns: The script result. It will have two fields: result and logs. Result will be the return value of the/
                        script. Logs will contain the content of anything logged from the console object by the script
        """

        response = self.mob_conn.execute_driver(script=textwrap.dedent(script), timeout_ms=timeout_for_script)
        return response

    def take_screenshot_and_save(self, screenshot_path=config.screenshot_folder, screenshot_name=None):
        """
        Take a screenshot of the current viewport/window/page.

            Args:
                screenshot_path: Path where the screenshot needs to be saved
                screenshot_name: name of the screenshot

            Returns: object of the inherited page to facilitate method chaining
        """

        self.mob_conn.save_screenshot(screenshot_path + screenshot_name)
        return self

    def wait_mobile_element_invisible(self, locatorList, wait_time=10, polling_time=poll_frequency_time):
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

        element = None
        for locator in locatorList:
            try:
                element = WebDriverWait(self.mob_conn, wait_time, polling_time).until(
                    EC.invisibility_of_element(locator))
                break
            except:
                raise Exception("Identifying the element failed")
        if element is None:
            raise PyAutoExceptions("Identifying the element failed in " + str(self.__class__.__name__) +
                                   " page, check the error logs for more info")
        return self

    def set_permission_ios(self, bundleId, services):
        """
        Will set the permissions for all the services for a specific application

            Args:
                bundleId: The bundle identifier of the destination app
                services: One or more access rules to set in dictionary format [E.g.: {'all': 'yes'}]
                            Refer: all (Apply the action to all services), calendar (Allow access to calendar), \
                                contacts-limited (Allow access to basic contact info), contacts (Allow access to full \
                                contact details), location (Allow access to location services when app is in use), location\
                                -always (Allow access to location services at all times)

            Returns: The object of the class itself to support method chaining

        """
        params = {"bundleId": bundleId, "access": services}
        self.mob_conn.execute_script("mobile: setPermission", params)
        return self

    # def scroll_to_text(self, text):
    #     """
    #
    #         Args:
    #             text:
    #
    #     Returns:
    #
    #     """
    #     try:
    #         element = self.mob_conn.find_element_by_android_uiautomator(
    #             'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().text("' + text + '").instance(0));')
    #         return element
    #     except NoSuchElementException:
    #         logger.error('it was not found')
    #         return None
    #     except Exception as e:
    #         logger.error("Unexpected error:")
    #         logger.exception(e)
    #         return None
