import dataclasses
from dataclasses import dataclass
import re
import requests

QUERY_TEMPLATE = """mutation {{      
    getDatasetStatistics(
        input: {input_fields} 
    )
    {{        
        datasetStatisticsResponses {{
            {output_fields}      
        }}
    }}
}}
"""


@dataclass
class Request:
    """
    This is a dataclass used to represent the GraphQL input needed for API requests.  Useful for
    those that don't want to learn the syntax of GraphQL.
    """

    longitude: int = 0
    latitude: int = 0
    country: str = ''
    city: str = ''
    address: str = ''
    warmingScenario: str = ''
    datasetId: int = 0
    output_fields: list = ()

    def build_query(self):
        """
        Builds a GraphQL query based on dataclasses' attributes.
        :return:
        """
        input_dict = dataclasses.asdict(self)
        output_fields = input_dict.pop('output_fields')
        return build_query(input_fields=input_dict, output_fields=output_fields)


def _get_group(matchobj):
    """
    Used to parse out dictionary pairs into the GraphQL format.  It essentially strips out single quotes when
    not needed.
    :param matchobj: the matched dictionary pair string parsed by the regular expression.
    :return:  GraphQL formatted dictionary pair
    """
    # print(matchobj.group(2))
    if matchobj.group(2) == '':
        # print('value')
        return matchobj.group(0)
    else:
        # print('key')
        return matchobj.group(1) + matchobj.group(2)


def build_query(input_fields={}, output_fields=[]):
    """
    Builds GraphQL query based on input and output requests fields.
    :param input_fields:  dictionary of inputs sent to the API.
    :param output_fields: array of output fields that the user wants returned.
    :return:  fully formatted GraphQL request.
    """
    # formatted_input = {key.replace('\'', ''): val for key, val in input_fields.items()}
    input_fields = re.sub("'(.*?)'(:?)", _get_group, str(input_fields))
    input_fields = input_fields.replace("'", "\"")
    return QUERY_TEMPLATE.format(input_fields=input_fields, output_fields='\n\t'.join(output_fields))


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
        :param query:  Either a fully formed GraphQL request string or a Request dataclass object.
        :param input_fields:  Used if query is not supplied.  Dictionary of inputs sent to the API.
        :param output_fields: Used if query is not supplied.  Array of output fields that the user wants returned.
        :return:  GraphQL response from the API.
        """
        print(type(query))
        if query is None:
            query = build_query(input_fields=input_fields, output_fields=output_fields)
        elif isinstance(query, Request):
            query = query.build_query()

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



