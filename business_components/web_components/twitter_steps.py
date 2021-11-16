from object_repository.pages.TwitterLoginPage import TwitterLogin
from PyAuto.PyAutoLogger import get_logger
import allure

logger = get_logger()


@allure.step("login to the twitter page")
def login_twitter(driver, user_name, password):
    TwitterLogin(driver).login(user_name, password)
