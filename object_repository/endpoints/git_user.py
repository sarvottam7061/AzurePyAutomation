from PyAuto.PyAutoRest import PyRest


# Using endpoints improves code maintenance and readability
class GitUser(PyRest):

    def __init__(self, rest_client):
        # call super class constructor, to inherit the self.response instance variable
        super().__init__()
        self.rest_client = rest_client  # PyRest object
        self.end_point = "https://api.github.com/user"  # you can also define the entire url here

    def user_response_authenticate(self, user_name, token):
        # to do authentication along with the request
        self.rest_client.get(self.end_point, auth=(user_name, token))
        return self.rest_client
