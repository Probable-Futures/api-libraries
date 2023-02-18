import requests
import input


class ProbableFutures:

    _user = None
    _password = None
    _access_token = None

    def __init__(self, user=None, password=None):
        self.configure(user=user, password=password)

    def configure(self, user=None, password=None):
        if user is not None:
            self._user = user
        if password is not None:
            self._password = password

    def connect(self, user=None, password=None):
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



