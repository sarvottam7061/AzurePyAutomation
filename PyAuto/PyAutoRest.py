import json
import re
import allure
import requests
from PyAuto.PyAutoReadWrite import ReadWrite
from PyAuto.PyAutoException import PyAutoExceptions
import jsonpath

try:
    from config import TestConfig as config

    test_data_path = config.testDataPath
except:
    test_data_path = None


class PyRest(requests.Session):

    def __init__(self, url=None):
        """
        Creates a rest_client to access different rest methods. Acts as a wrapper for requests module

            Args:
                url: string -> not mandatory
        """
        super().__init__()
        self.response = None
        self.url = url

    def _get_url(self, url):
        """
        Get completed url, by checking if only endpoint(api/users) or the url and endpoint is passed

            Args:
                url: string-> endpoint or the complete url with endpoint

            Returns: string-> the complete url with endpoint

        """
        if url.startswith("http"):
            return url
        else:
            if self.url:
                return self.url + url
            else:
                raise PyAutoExceptions("Use the complete url or create PyRest object with app url")

    def get(self, url, **kwargs):
        """
        To get some details on resources, overrides get request from requests.session library

            Args:
                url: can pass only api endpoint or the complete url
                **kwargs: refer requests.get method from requests module

            Returns: rest_client or PyRest object for method chaining

        """
        url = self._get_url(url)
        self.response = super().get(url, **kwargs)
        return self

    def post(self, url, data=None, json=None, **kwargs):
        """
        To create new resource in backend api, overrides post in requests.Session library

            Args:
                url: can pass only api endpoint or the complete url
                data: data as request body
                json: json as request body
                **kwargs: refer requests.get method from requests module

            Returns: rest_client or PyRest object for method chaining

        """
        url = self._get_url(url)
        self.response = super().post(url, data=data, json=json, **kwargs)
        return self

    def put(self, url, data=None, **kwargs):
        """
        Updates resource in backend api, overrides put in requests.Sessions library

            Args:
                url: can pass only api endpoint or the complete url
                data: data as request body
                **kwargs: refer requests.post method from requests module

            Returns: rest_client or PyRest object for method chaining

        """
        url = self._get_url(url)
        self.response = super().put(url, data=data, **kwargs)
        return self

    def patch(self, url, data=None, **kwargs):
        """
        Updates resource in backend api, overrides patch in requests.Session library

            Args:
                url: can pass only api endpoint or the complete url
                data: data as request body
                **kwargs: refer requests.put method from requests module

            Returns: rest_client or PyRest object for method chaining

        """
        url = self._get_url(url)
        self.response = super().patch(url, data=data, **kwargs)
        return self

    def delete(self, url, **kwargs):
        """
        Delete a resource in backend api, overrides delete in requests.Session library

            Args:
                url: can pass only api endpoint or the complete url
                **kwargs: refer requests.delete method from requests module

            Returns: rest_client or PyRest object for method chaining

        """
        url = self._get_url(url)
        self.response = super().delete(url, **kwargs)
        return self

    def head(self, url, **kwargs):
        """
        Sends a HEAD request. overrides head in requests.Session library.

            Args:
                url: URL for the new :class:`Request` object.
                **kwargs: Optional arguments that ``request`` takes.

            Returns: rest_client or PyRest object for method chaining

        """
        url = self._get_url(url)
        self.response = super().head(url, **kwargs)
        return self

    def validate_response_json(self, json_expected):
        """
        Asserts if the response.json() is equal to the json expected passed

            Args:
                json_expected: send the expected json that should be received as response

            Returns: rest_client or PyRest object for method chaining

        """
        assert self.response.json() == json_expected, f"The json expected value {json_expected} did not match the response json body {self.response.json()}"
        return self

    def validate_response_json_file(self, path_to_file):
        """
        Validate json with the response from file

            Args:
                path_to_file: path to the file where expected json is present

            Returns: rest_client or PyRest object for method chaining

        """
        json_from_file = ReadWrite.load_json_file(path_to_file)
        assert self.response.json() == json_from_file, f"The json read from file {json_from_file} did not match the response json body {self.response.json()} "
        return self

    def validate_response_json_key_value(self, json_key, value):
        """
        Validate the value against the json key

            Args:
                json_key: key to parse the json response
                value: value to be validated against

            Returns: rest_client or PyRest object for method chaining

        """
        assert self.response.json()[
                   json_key] == value, f"The response value {self.response.json()[json_key]} did not match with the value sent {value}"
        return self

    def validate_json_path_value(self, path, value):
        """
        Validate the json value, by parsing using json

            Args:
                path: path value to be sent to jsonpath -> uses a special style syntax in jsonpath eg:$.data[*].id
                value: value to be validated against once the json path returns the value, value should be sent as a list
                       eg: ['hello'] or ['testing', 'tester'] or [1, 2, 3, 4, 6].
            Returns: rest_client or PyRest object for method chaining

        """
        parsed_value = jsonpath.jsonpath(self.response.json(), path)
        assert parsed_value == value, f"The response value {parsed_value}, parsed using {path} " \
                                      f"the path did not match with the value sent {value}"
        return self

    def validate_response_status_code(self, status_code_expected):
        """
        Validate the response code received fromt he last request response

            Args:
                status_code_expected: status code expected from the response

            Returns: rest_client or PyRest object for method chaining

        """
        assert self.response.status_code == status_code_expected, f"The response status code {self.response.status_code} did not " \
                                                                  f"match the expected status code {status_code_expected}"
        return self

    def write_json(self, fileName, filePath=test_data_path):
        """
        Write the json file into test data path

            Args:
                fileName: name of the file with .json extension
                filePath: path to save json file in, defaults to test data path in pyautomation framework, if using
                          pyauto package, the default value is None and should be overridden if not the json file to be in same
                          folder as execution

            Returns: rest_client or PyRest object for method chaining

        """
        if filePath:
            with open(filePath + fileName, 'w') as f:
                json.dump(self.response.json(), f)
        else:
            with open(fileName, 'w') as f:
                json.dump(self.response.json(), f)
        return self

    def validate_response_header_key_value(self, key, value):
        """
        Validate the header key and value

            Args:
                key: key to be parsed in the header
                value: expected value to be validated against

            Returns: rest_client or PyRest object for method chaining

        """
        assert self.response.headers[key] == value, f'expected value {value} did not match {self.response.headers[key]}'
        return self

    def validate_response_header_json(self, expected_json):
        """
        Validate the response header in json

            Args:
                expected_json: expected json to be compared against response.headers

            Returns: rest_client or PyRest object for method chaining

        """
        assert self.response.headers == expected_json, f'expected json {expected_json} did not match {self.response.headers}'
        return self

    # ----------------------------------------------------------------------------------------------------

    def get_all_headers(self):
        """
        Get all the headers of the response

            Returns: rest_client or PyRest object for method chaining

        """
        # print(self.response.headers)
        return self.response.headers

    def get_header_value(self, key):
        """
        Gets the header value from the key given.

            Args:
                key: the key from the headers

            Returns: the value of the key

        """
        try:
            # print(self.response.headers[key])
            return self.response.headers[key]
        except:
            raise PyAutoExceptions(f"The header {key} is not present")

    def set_header(self, key, new_value):
        """
        Will set a new value for the key in header (E.g.: [key]:[value])

            Args:
                key: the key in the header
                value: the value for the key to be set

            Returns: rest_client or PyRest object for method chaining

        """
        if self.response.headers[key]:
            current_value = self.response.headers[key]
            print("Current Value is: ", current_value, " ,New Value is:", new_value)
        self.response.headers[key] = new_value
        return self

    def get_response_time(self):
        """
        Will get the time elapsed between the request and response

            Returns: the time elapsed in SECONDS

        """
        # print(self.response.elapsed.total_seconds())
        return self.response.elapsed.total_seconds()

    def get_response_type(self):
        """
        Will get the type of response from the headers of the request

            Returns: the response type in string

        """
        try:
            print(self.response.headers["Content-Type"])
            return self.response.headers["Content-Type"]
        except:
            raise PyAutoExceptions("Could not determine the response type")

    def get_response_timestamp(self):
        """
        Will get the complete time-stamp of the request(the moment it was made) in GMT zone

            Returns: the complete time-stamp in string

        """
        try:
            # print(self.response.headers["Date"])
            return self.response.headers["Date"]
        except:
            raise PyAutoExceptions("Could not determine the response time-stamp")

    def response_header_should_not_match_key_value(self, key, value):
        """
        validate the (key:value) pair should not match with the header (key:value) pair

            Args:
                key: key parsed in the header
                value: expected value to be validated against

            Returns: rest_client or PyRest object for method chaining

        """
        assert self.response.headers[key] != value, f'expected value {value} matched {self.response.headers[key]}'
        return self

    def get_response_cookies(self):
        """
        Will get all the cookies of the response

            Returns: all_cookies in a dictionary format (i.e:[Key]:[Value])

        """
        all_cookies = self.response.cookies.get_dict()
        # print(all_cookies)
        return all_cookies

    def validate_cookie_value(self, cookie_key, expected_value):
        """
        Validate the expected value of the cookie with its actual value from the request

            Args:
                cookie_key: cookie Name
                expected_value: value of the Cookie to be validated

            Returns: rest_client or PyRest object for method chaining

        """
        all_cookies = self.get_response_cookies()
        assert all_cookies.get(
            cookie_key) == expected_value, f'Expected value was {expected_value} but got {all_cookies.get(cookie_key)}'
        return self

    def get_cookie_value(self, cookie_key):
        """
        Get the value of a particular cookie from the request

            Args:
                cookie_key: cookie Name

            Returns: value of the cookie

        """
        all_cookies = self.get_response_cookies()
        try:
            cookie_val = all_cookies.get(cookie_key)
            return cookie_val
        except:
            raise PyAutoExceptions("Could not determine the cookie")

    def match_should_contain_json_key(self, json_key):
        """
        Asserts if the Response contains the JSON key

            Args:
                json_key: key in the json response to be validated

            Returns: rest_client or PyRest object for method chaining

        """
        print(self.response.json())
        assert json_key in self.response.json(), f'The key {json_key} is not present'
        return self

    def match_should_not_contain_json_key(self, json_key):
        """
        Asserts if the Response DOES NOT contain the JSON key

            Args:
                json_key: key in the json response to be validated

            Returns: rest_client or PyRest object for method chaining

        """
        assert json_key not in self.response.json(), f'The key {json_key} is present'
        return self
