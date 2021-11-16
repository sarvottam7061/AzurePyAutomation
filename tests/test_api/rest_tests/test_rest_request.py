import requests
from PyAuto.PyAutoRest import PyRest
from config import TestConfig as config
import pytest
from PyAuto.PyAutoLogger import get_logger
from business_components.api_components.reqres_components import *

logger = get_logger()
from utilities.helper import parametrized_test_data_json_fetch
import allure


@pytest.mark.get_request
def test_user_list(rest_client):
    validate_total_number_of_page(rest_client, 'total_pages', 2)
    validate_last_name_page2_item_2(rest_client, '$.data[1].last_name', ['Ferguson'])
    validate_list_of_id_page_2(rest_client, '$.data[*].id', [7, 8, 9, 10, 11, 12])


@pytest.mark.parametrize("json_data,", parametrized_test_data_json_fetch(config.testDataFileName, 'TC-04'))
@pytest.mark.post_request
def test_create_user(rest_client, json_data):
    # if you have single data parametrization(only json_data), we will get a tuple and it has to be converted by indexing
    # or using object destruction *json_data
    # if len(json_data)==1:
    #     json_data= json_data[0]
    validate_user_creation(rest_client, *json_data)


@pytest.mark.authenticate
def test_authenticate_git(rest_client):
    authenticate_git_user(rest_client, user_name="user", token="personal access token generated from git")

# ----------------------------------------------------------------------------


@pytest.mark.get_all_headers
def test_get_headers(rest_client):
    get_headers(rest_client)


@pytest.mark.get_headers_from_key
def test_get_header_from_key(rest_client):
    get_header_from_key(rest_client, "Content-Type")


@pytest.mark.get_response_time_elapsed
def test_get_response_time(rest_client):
    get_time_elapsed(rest_client)


@pytest.mark.get_all_cookies
def test_get_all_cookies(rest_client):
    get_the_cookies(rest_client)


@pytest.mark.match_should_contain_key
def test_response_should_contain_key(rest_client):
    should_contain_key(rest_client, "per_page")
    
@pytest.mark.post_user
def test_post_user(rest_client):
    validate_post_user_creation(rest_client)
    
    
