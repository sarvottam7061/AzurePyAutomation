from config import TestConfig as config
from PyAuto.PyAutoLogger import get_logger
from PyAuto.PyAutoReadWrite import ReadWrite
from object_repository.endpoints.api_users import ApiUsers
from object_repository.endpoints.git_user import GitUser
import allure

logger = get_logger()  # get the logger, which will add logs to allure reports as well


# steps for rest api testing
# best practice to add @allure.step for more insights in allure reports

@allure.step("validate the user last name from reqres")
def validate_last_name_page2_item_2(rest_client, path, value):
    # used method chaining
    # ApiUsers is the endpoint and rest_client is a session created from PyRest
    ApiUsers(rest_client).get_users_page_2().validate_response_status_code(200). \
        validate_json_path_value(path, value)  # json path helps in parsing the json response


@allure.step("validate the list of user id from reqres")
def validate_list_of_id_page_2(rest_client, path, value):
    # write json will write the response received from the request as a json file
    ApiUsers(rest_client).get_users_page_2().validate_response_status_code(200). \
        validate_json_path_value(path, value).write_json('employee_page2.json')


@allure.step("validate total page reqres")
def validate_total_number_of_page(rest_client, key, value):
    # you can also validate the json based on key value pair
    ApiUsers(rest_client).get_users_page_2().validate_response_status_code(200). \
        validate_response_json_key_value(key, value)


@allure.step("validate if the user is created in system")
def validate_user_creation(rest_client, json_data):
    ApiUsers(rest_client).post_user(json_data).validate_response_status_code(201). \
        validate_response_json_key_value('name', json_data['name'])


@allure.step("validate the user id based on the id fetched from the response")
def validate_user_id(rest_client):
    # read json file and parse id value, send it along with endpoint url
    json_data = ReadWrite.load_json_file(config.testDataPath + 'employee_page2.json')
    id_2 = json_data['data'][0]['id']
    ApiUsers(rest_client).get_user_id(id_2).validate_response_status_code(200). \
        validate_response_json_path_value("$.data.fname")


@allure.step("read and return excel first name value")
def read_excel_first_name():
    # reading a value from excel sheet
    excel_reader = ReadWrite(config.testDataPath, "names.xlsx")
    data_frame = excel_reader.load_excel("name")
    value = excel_reader.read_excel_cell_row_column(data_frame, 0, "First Name")
    return value


# you can directly call a different url using rest client
@allure.step("Authenticate git user with dummy data, bound to fail")
def authenticate_git_user(rest_client, user_name, token):
    # you can send the complete url config.api_url or just the end point.
    # In GitUser the complete url is described as endpoint
    GitUser(rest_client).user_response_authenticate(user_name, token).validate_response_status_code(200)

# -----------------------------------------------------------------------


@allure.step("Get all the headers of the response")
def get_headers(rest_client):
    all_header = ApiUsers(rest_client).get_users_page_2().validate_response_status_code(200).get_all_headers()
    print(all_header)


@allure.step("Get the header value from the key of response")
def get_header_from_key(rest_client, key):
    print(ApiUsers(rest_client).get_users_page_2().validate_response_status_code(200).get_header_value(key))


@allure.step("Get the response time")
def get_time_elapsed(rest_client):
    time_taken = ApiUsers(rest_client).get_users_page_2().validate_response_status_code(200).get_response_time()
    print(time_taken)


@allure.step("Get all the cookies")
def get_the_cookies(rest_client):
    cookies = ApiUsers(rest_client).get_users_page_2().validate_response_status_code(200).get_response_cookies()
    print(cookies)


@allure.step("Match contains JSON key")
def should_contain_key(rest_client, json_key):
    ApiUsers(rest_client).get_users_page_2().validate_response_status_code(200).match_should_contain_json_key(json_key)



# @allure.step("Validate Cookie")
# def get_the_cookies(rest_client, cookie_key, expected_value):
#     ApiUsers(rest_client).get(url="https://www.google.com/").validate_cookie_value(cookie_key, expected_value)

@allure.step("post valid data")
def validate_post_user_creation(rest_client):
    excel_test_data = ReadWrite(config.testDataPath, "names_new.xlsx")
    edf = excel_test_data.load_excel("name")
    data = {
        "name": edf['First Name'][0] + edf['Last Name'][0],
        "job": "leader"}
    ApiUsers(rest_client).post_user(data).validate_response_status_code(201).validate_response_json_key_value('name', data['name'])
