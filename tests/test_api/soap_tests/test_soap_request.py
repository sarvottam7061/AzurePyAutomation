import allure
import pytest
from config import TestConfig as config
from PyAuto.PyAutoReadWrite import ReadWrite
from utilities.helper import convert_to_json, read_json_for_soap, parametrized_test_data_json_fetch

from PyAuto.PyAutoLogger import get_logger

logger = get_logger()


@pytest.mark.soap_tests
@allure.step("get and save list of countries")
def test_get_list_of_countries(soap_client):
    response = soap_client.service.ListOfCountryNamesByName()
    assert len(response) == 246
    assert response[1]['sName'] == "Afghanistan"
    response = convert_to_json(response)
    ReadWrite.write_json(response, "listOfCountries.json")


@pytest.mark.soap_tests
@allure.step("retrieve country code and validate capital")
def test_retrieve_country_code_validate_capital(soap_client):
    request_values = read_json_for_soap("listOfCountries.json")
    response = soap_client.service.CapitalCity(request_values['India'])
    assert response == "New Delhi"


@pytest.mark.soap_test_data_driven
@allure.step("retrieve country code and validate capital")
@pytest.mark.parametrize("country, capital", parametrized_test_data_json_fetch("TestData.json", "TC-03"))
def test_retrieve_country_code_validate_capital_parametrized(soap_client, country, capital):
    request_values = read_json_for_soap("listOfCountries.json")
    response = soap_client.service.CapitalCity(request_values[country])
    assert response == capital
