from PyAuto.PyAutoLogger import get_logger

logger = get_logger()


def handle_selenium_exception(exception, locator=None):
    """
    Handle all sorts of selenium exception and log the same in report

        Args:
            exception: exception object that is captured
            locator: defaults to None, can pass the locator to display locator in logs

        Returns: logs the exception info into the report
    """
    exception_name = str(exception.__class__.__name__)
    exception_message = str(exception).rstrip("\n")
    locator_strategy = None
    if locator:
        locator_strategy = "by " + str(locator[0]) + " " + str(locator[1])
    if exception_name == "NoSuchElementException":
        logger.error(exception_name + ": " + exception_message + " " + locator_strategy)
        logger.info("hello world")
    elif exception_name == "WebDriverException":
        logger.error(exception_name + ": " + exception_message)
    elif exception_name == "ElementClickInterceptedException":
        logger.error(exception_name + ": " + exception_message + " " + locator_strategy)
    elif exception_name == "ElementNotInteractableException":
        logger.error(exception_name + ": " + exception_message + " " + locator_strategy)
    elif exception_name == "ElementNotSelectableException":
        logger.error(exception_name + ": " + exception_message + " " + locator_strategy)
    elif exception_name == "InsecureCertificateException":
        logger.error(exception_name + ": " + exception_message)
    elif exception_name == "InvalidArgumentException":
        logger.error(exception_name + ": " + exception_message)
    elif exception_name == "InvalidCookieDomainException":
        logger.error(exception_name + ": " + exception_message)
    elif exception_name == "InvalidCoordinatesException":
        logger.error(exception_name + ": " + exception_message)
    elif exception_name == "InvalidElementStateException":
        logger.error(exception_name + ": " + exception_message)
    elif exception_name == "InvalidSelectorException":
        logger.error(exception_name + ": " + exception_message + " " + locator_strategy)
    elif exception_name == "InvalidSwitchToTargetException":
        logger.error(exception_name + ": " + exception_message + " " + locator_strategy)
    elif exception_name == "MoveTargetOutOfBoundsException":
        logger.error(exception_name + ": " + exception_message + " " + locator_strategy)
    elif exception_name == "NoAlertPresentException":
        logger.error(exception_name + ": " + exception_message + " " + locator_strategy)
    elif exception_name == "NoSuchAttributeException":
        logger.error(exception_name + ": " + exception_message + " " + locator_strategy)
    elif exception_name == "NoSuchCookieException":
        logger.error(exception_name + ": " + exception_message + " " + locator_strategy)
    elif exception_name == "TimeoutException":
        logger.error(exception_name + ": " + exception_message + " " + locator_strategy)
    else:
        logger.error(exception_name + ": " + exception_message)


class PyAutoExceptions(Exception):

    def __init__(self, message):
        """
        Customized exception class for pyautomation framework

            Args:
                message: Message to be thrown along with exception

        """
        self.message = message
        super().__init__(self.message)
