import unittest
import json
import requests_mock

from src.scrapper import Scrapper

class TestScrapper(unittest.TestCase):

    def setUp(self):
        self.scrapper = Scrapper()

        # Saving the requests_mock as an object to reuse it in the class
        with requests_mock.Mocker() as mock:
            self.requests_mock = mock
            self.mock_requests()

    def mock_requests(self):
        """Mocking all the URLs we'll use on this test class"""
        names_endpoint = 'https://www.khuxbot.com/api/v1/medal?q=names'
        names_fixture_file = 'test/fixtures/scrapper/medal_names.json'
        with open(names_fixture_file) as fixture:
            names_response = json.loads(fixture.read())
        self.requests_mock.get(names_endpoint, json=names_response)

    def test_get_medal_names(self):
        expected_names_file = 'test/fixtures/scrapper/medal_names.txt'
        with open(expected_names_file) as content:
            expected_names = [name.strip() for name in content.readlines()]

        with self.requests_mock:
            self.assertListEqual(self.scrapper.get_medal_names(), expected_names)

