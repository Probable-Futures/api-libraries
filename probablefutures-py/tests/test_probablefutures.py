import dataclasses
import os
import unittest

from probablefutures import probablefutures
from probablefutures import ProbableFutures
from probablefutures import Request


class TestProbableFutures(unittest.TestCase):

    _user = os.getenv('PF_USER')
    _password = os.getenv('PF_PASSWORD')

    def test_init(self):
        pf = ProbableFutures()
        self.assertEqual(pf._user, None)
        self.assertEqual(pf._password, None)

        pf = ProbableFutures(user='foo')
        self.assertEqual(pf._user, 'foo')
        self.assertEqual(pf._password, None)

        pf = ProbableFutures(password='foo')
        self.assertEqual(pf._user, None)
        self.assertEqual(pf._password, 'foo')

        pf = ProbableFutures(user='foo', password='bar')
        self.assertEqual(pf._user, 'foo')
        self.assertEqual(pf._password, 'bar')

    def test_raw_init(self):
        import requests
        response = requests.post('https://probablefutures.us.auth0.com/oauth/token',
                                 json={"client_id": self._user, "client_secret": self._password, "audience": "https://graphql.probablefutures.com", "grant_type": "client_credentials"})
        access_token = response.json()['access_token']
        print(access_token)

    def test_configure(self):
        pf = ProbableFutures()
        pf.configure(user='foo', password='bar')
        self.assertEqual(pf._user, 'foo')
        self.assertEqual(pf._password, 'bar')

    def test_connect(self):
        pf = ProbableFutures()
        pf.configure(user=self._user, password=self._password)
        pf.connect()

        pf = ProbableFutures()
        pf.connect(user=self._user, password=self._password)

    def test_request(self):
        pf = ProbableFutures(self._user, password=self._password)
        pf.connect()
        request = """mutation {      
            getDatasetStatistics(
                input: {
                    longitude: -73.9, 
                    latitude: 40.7, 
                    country: "US",
                    warmingScenario: "1.0", 
                    datasetId: 40104
                }) 
            {        
                datasetStatisticsResponses {
                    datasetId
                    highValue     
                    lowValue          
                    midValue          
                    name        
                    unit          
                    warmingScenario      
                }
            }
        }
        """
        response = pf.request(query=request)
        response_json = response.json()
        print(response_json)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json['data'])

        input_fields = {
            "longitude": -73.90,
            "latitude": 40.7,
            "warmingScenario": "1.0",
            "datasetId": 40104
        }
        output_fields = ["datasetId", "highValue", "lowValue", "midValue", "name", "unit", "warmingScenario"]
        response = pf.request(input_fields=input_fields, output_fields=output_fields)
        response_json = response.json()
        print(response_json)
        self.assertEqual(response.status_code, 200)


    def test_request2(self):
        input_fields = {
            "longitude": -73.90,
            "latitude": 40.7,
            "warmingScenario": "1.0",
            "datasetId": 40104
        }
        output_fields = ["datasetId", "highValue", "lowValue", "midValue", "name", "unit", "warmingScenario"]
        print(probablefutures.build_query(input_fields=input_fields, output_fields=output_fields))

    def test_request3(self):
        request = Request()
        request.longitude = -73.90
        request.warmingScenario = "1.0"
        request.datasetId = 40104
        request.output_fields = ["datasetId", "highValue", "lowValue", "midValue", "name", "unit", "warmingScenario"]
        print(request)
        print(dataclasses.asdict(request))
        print(request.build_query())
        print(isinstance(request, Request))

    def test_request4(self):
        request = Request()
        request.longitude = -73.90
        request.warmingScenario = "1.0"
        request.datasetId = 40104
        request.output_fields = ["datasetId", "highValue", "lowValue", "midValue", "name", "unit", "warmingScenario"]
        pf = ProbableFutures(self._user, password=self._password)
        pf.connect()
        response = pf.request(request)
        response_json = response.json()
        print(response_json)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json['data'])


if __name__ == '__main__':
    unittest.main()
