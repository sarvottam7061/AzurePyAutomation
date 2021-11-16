import platform
import os

# test url
web_url = "https://demo.seleniumeasy.com/"  # traditional test
bdd_url = "https://demo.seleniumeasy.com/"
# bdd_url = "http://sampleapp.tricentis.com/101/"  # bdd styled tests
rest_url = "https://reqres.in/"  # rest api url
wsdl_url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL"  # soap test wsdl
# Database engine string for connection
# db_uri = 'postgresql://postgres:455546@localhost:5432/dvdrental'  # for postgres
# db_uri = 'mysql://root:455546@localhost:3306/dvd' #for mysql
db_uri = 'sqlite:///../../resources/movies.db'  # for sqlite
# db_uri = 'mssql://scott:tiger@hostname:port/dbname' #for mssql
# db_uri = 'oracle://scott:tiger@127.0.0.1:1521/sidname'# for oracle database
# db_uri = 'mariadb://user:pass@some_mariadb/dbname' #for maria database

# Browser settings
# values = chrome or edge or firefox or ie or remote
browser = "chrome"
manage_driver = True
# Path to Driver
safari_driver = "/usr/bin/safaridriver"
chrome_driver = "../../drivers/chromedriver.exe"
gecko_driver = "../../drivers/geckodriver.exe"
ie_driver = "../../drivers/iedriver.exe"
edge_driver = "../../drivers/edgedriver.exe"

# options to be added - ci refers to jenkins or docker execution
chromeOptions = {'local': ['--start-maximized', '--disable-extensions'],
                 'ci': ['--disable-extensions', '--headless', '--no-sandbox', '--disable-gpu',
                        '--window-size=1920,1200']}
fireFoxOptions = {'local': ['--disable-extensions'],
                  'ci': ['--headless']}
edgeOptions = {'local': ['--start-maximized'],
               'ci': ['--headless']}
IEOptions = {'local': ['--start-maximized'],
             'ci': ['--headless']}
# chromeOptions = ('disable-extensions', 'start-maximized', 'headless')
# remote execution
remoteOptions = {"url": "http://selenium-hub:4444/wd/hub"}
desiredCapabilities_chrome = {"browserName": "chrome", "browserVersion": 91.0, "platform": "windows"}
desiredCapabilities_firefox = {"browserName": "firefox", "browserVersion": "89.0", "platform": "LINUX"}
desiredCapabilities_remote = desiredCapabilities_firefox


#Windows Desktop Automation settings
# desktop_app_path = "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App"  # calculator # "calculator.exe"
# desktop_app_title = "Calculator"
# desktop_engine = "winappdriver"

desktop_app_path = r"C:/Program Files (x86)/SAP/FrontEnd/SAPgui/saplogon.exe"  # SAP APP
desktop_app_title = "SAPLogon750"
desktop_engine = "pywinauto"

# desktop_app_path = "AD2F1837.HPPOSDemo_v10z8vjag6ke6!App"  # HP POS APP
# desktop_app_title = "HPPOSDEMO"
# desktop_engine = "winappdriver"

winapp_driver_url = "http://127.0.0.1:4723"
winapp_driver_cap = desired_caps = {
    "app": desktop_app_path
}
# winapp_server_path = r'start cmd /c "C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"'


# Mobile Automation Settings

mob_udid = 'ZY2243HFS7'  # UDID specific for every mobile device
mob_platform = 'android'  # Mobile OS
mob_remote_url = 'http://localhost:4723/wd/hub'  # Remote URL for the connection

# --- Android DC --------
# desiredCapabilities_mobile = {'platformName': 'android', 'platformVersion': '8.1.0', 'deviceName': 'Moto G (5) Plus',
#                               'udid': 'ZY2243HFS7', 'appPackage': 'com.solodroid.solomerce',
#                               'appActivity': 'com.solodroid.solomerce.activities.ActivitySplash',
#                               'automationName': 'UIAutomator2', 'noReset': 'True'}
# desiredCapabilities_mobile = {'platformName': 'android', 'platformVersion': '8.1.0', 'deviceName': 'Moto G (5) Plus', 'udid': 'ZY2243HFS7', 'browserName': 'Chrome', 'automationName': 'UIAutomator2', 'noReset': 'True', 'autoWebview': 'true'}
# desiredCapabilities_mobile = {'platformName': 'android', 'platformVersion': '8.1.0', 'deviceName': 'Moto G (5) Plus', 'udid': 'ZY2243HFS7', 'appPackage': 'com.flipkart.android', 'appActivity': 'com.flipkart.android.SplashActivity', 'automationName': 'UIAutomator2', 'noReset': 'True'}

# ----- iOS DC ----------
# desiredCapabilities_mobile = {'udid': '00008030-001C2D64027B802E', 'platformName': 'ios','deviceName': 'Prateek\'s iPhone', 'platformVersion': '14.7.1', 'automationName': 'XCUITest', 'bundleId': 'com.appflipkart.flipkart', 'noReset': 'false'}
# desiredCapabilities_mobile = {'udid': '00008030-001C2D64027B802E', 'platformName': 'ios', 'deviceName': 'Prateek\'s iPhone', 'platformVersion': '14.7.1', 'automationName': 'XCUITest', 'browserName': 'Safari', 'noReset': 'false', 'autoWebview': 'true'}


mobile_ipa_path = ''
mobile_apk_path = 'C:\\Users\\ASUS\\Downloads\\apk_mob\\ECommerce_Demo_v3.apk'
mobile_web_url = "https://www.seleniumeasy.com/test/"

appium_command = "start cmd /c appium"
node_close_command = "start cmd /c taskkill /F /IM node.exe"

# Folder Paths
# Path to test data folder
testDataPath = os.path.abspath("../../testData/") + "/"
# testDataPath = os.path.abspath("E:/automate/PyAutomation_Master_V1/testData/") + "/"
testDataFileName = "TestData.xlsx"
# testDataFileName = "TestData.json"
resourcesFolderPath = os.path.abspath("../../resources/") + "/"
# Screenshot path - has to be set when framework is set up
screenshot_folder = os.path.abspath("../../resources/screenshots/") + "/"
object_repo_path = os.path.abspath("../../resources/object_repo.db")

# wait times
# Explicit wait time to identify locators and poll time
explicit_wait = 5
poll_time = 0.2  # for each 0.5 second, the condition will be checked

# implicit wait during driver initialization
implicit_wait = 3

# Parallel Execution - no of Threads
parallel = False
thread_num = 3

# Flaky test flag
# Rerun Attempts for failed tests - set to 0 ->disabled
rerun_flaky_tests = 0

# Maximum failures in a run
max_fail = 100

# last run Failed tests rerun
last_failed_tests = False

# Reporting value - allure or html or both
ReportType = "allure"
ReportType_api = "allure"
ReportType_bdd = "allure"

# Shows the trends and history of runs for all test cases.
# Must be used only for fixed set of test cases that will be run after each release
Allure_History = False

# tags are marked over tests with @pytest.mark.<tag_name>


# --------------------------------------------------------------------------------------desktop app tests


# tags = ["right_click_element"]
# tags = ["test_screen_shot"]
# -------------------------------------------------------
tags = ["se_input_form"]
# tags = ["excel_data_driven_se"]
# tags = ["failed_test"]
# tags = ["bdd_selenium"]
# tags = ["excel_data_driven_se","failed_test"]
# tags = ["failed_test_except"]
# tags = ["se_input_form", "wait_and_fetch", "failed_test"]
# tags = ['bdd_selenium', 'bdd_e2e', 'e2e']
# tags = ['soap_tests']
# tags = ['soap_tests', 'soap_test_data_driven']
# tags = ['get_request', 'post_request', 'excel_data_driven_se']
# tags = ['e2e_rest']
# tags = ['bdd_e2e']

# tags = ["se_input_form", "excel_data_driven_se", "wait_and_fetch", "failed_test", "failed_test_except", 'bdd',
#         'soap_tests', 'soap_test_data_driven', 'get_request', 'post_request', 'authenticate', 'e2e_rest', 'bdd_e2e',
#         'db_tests']
# tags = ["e2e_rest_db"]
# -------------------- Mobile Tests --------------------
# tags = ["open_youtube", "clear_open_apps"]
# tags = ["demoTest_native"]
# tags = ["perform_actions"]
# tags = ["test_flipkart_ios"]  # flipkart native ios
# tags = ["test_ios_web"]  # SeleniumEasy web ios
# tags = ["test_home"]  # flipkart native ios
# tags = ["mobile_bdd"]
# tags = ["e2e_mobile"]
# tags = ["flipkart_search_iphone"]  # flipkart native android
# tags = ["swipe_image"]  # flipkart native android
# tags = ["nike_shoe_test", "checkout_test"]  # E-Commerce native android
# tags = ["mobile_orange"]  # OrangeHRM web android
# tags = ["mobile_orange_test2"]  # OrangeHRM web android test2
# tags = ["mobile_selenium_easy"]  # SeleniumEasy web android
#
# -------------------------------------------------------
# it can be set as empty list, to include all the files in subfolder of where RunTest is present

test_file_e2e = ['e2e_scripts/test_e2e.py', 'e2e_scripts/test_e2e_desktop.py']
# test_file_e2e = ['e2e_step_defs/test_step_def.py']
test_file_scripts = ["selenium_easy_tests/test_selenium_easy.py"]
test_file_bdd = ["auto_insurance_test/test_selenium_easy.py"]
test_file_api = ["soap_tests/test_soap_request.py", "rest_tests/test_rest_request.py"]
test_file_db = ["dvdrental_tests/test_actors_payment.py"]
test_file_mobile = ["mobile_tests/test_mobile.py"]
test_file_desktop = ["sap_windows_test/test_sap_windows.py"]

# set folder to empty to execute all tests in current and sub folders
# test_file_scripts = []

#run mode can be 'capture', 'heal', 'normal', 'capture&heal'
# run_mode = 'capture&heal'
run_mode = 'normal'
healing_score = 0.5
use_last_healed = False

#Failure Analysis
analyze_failures = True

