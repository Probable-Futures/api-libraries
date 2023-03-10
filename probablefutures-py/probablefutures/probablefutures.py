import requests
import input


class ProbableFutures:
    """
    ProbableFutures API Helper class that allows a user to easily connect and make requests to the Probable Futures
    API.  More documentation on the API can be found here:  https://probable-futures.github.io/docs/api/
    """

    _user = None
    _password = None
    _access_token = None

    def __init__(self, user=None, password=None):
        """
        Initialize the API class using optional user/password combination.
        :param user:
        :param password:
        """
        self.configure(user=user, password=password)

    def configure(self, user=None, password=None):
        """
        Configure the class to use user/password combination for all future requests.
        :param user:
        :param password:
        """
        if user is not None:
            self._user = user
        if password is not None:
            self._password = password

    def connect(self, user=None, password=None):
        """
        Make initial connection to Probable Futures API.  By default, it will attempt to use pre-configured
        user/password combination.  If user/password is provided as parameters, these will override any existing
        configuration and be used when attmepting to connect.
        :param user:
        :param password:
        """
        self.configure(user=user, password=password)
        body = {
            "client_id": self._user,
            "client_secret": self._password,
            "audience": "https://graphql.probablefutures.com",
            "grant_type": "client_credentials"
        }
        response = requests.post('https://probablefutures.us.auth0.com/oauth/token', json=body, )
        self._access_token = response.json()['access_token']

    def request(self, query=None, input_fields={}, output_fields=[]):
        """
        Make a request to the API.  Assumes the connect() call has been made prior to this call.  User can provide
        either the raw query or a dictionary of input fields and array of output fields used to construct a json query.
        :param query:
        :param input_fields:
        :param output_fields:
        :return:
        """
        if query is None:
            query = input.build_query(input_fields=input_fields, output_fields=output_fields)

        print(query)
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self._access_token
        }
        gql_query = {
            "query": query,
            "variables": {}
        }
        response = requests.post('https://graphql.probablefutures.org/graphql', headers=headers, json=gql_query)
        return response



