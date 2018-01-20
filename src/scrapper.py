import requests
from urllib.parse import urlencode

from src.db import DBWrapper


class Scrapper:

    def __init__(self):
        self.medal_base_endpoint = 'https://www.khuxbot.com/api/v1/medal'

    def get_medal_names(self):
        response = requests.get(self.medal_base_endpoint, params={"q": "names"})
        return (response.json())['names']

    def get_medals(self, medal_name):
        """Returns a list of medals matching the specified search"""

        # We need to prepare the request manually, as we need to encode spaces
        # as '%20' instead of as the by-default '+'
        params = {"q": "data", "medal": medal_name}
        encoded_params = urlencode(params).replace('+', '%20')

        session = requests.Session()
        request = requests.Request(method='GET', url=self.medal_base_endpoint)
        prepared = request.prepare()
        prepared.url += '?' + encoded_params
        response = session.send(prepared)

        if 'error' in response.json():
            return []

        medals_dict = response.json()['medal']
        medals = []
        for index, medal in medals_dict.items():
            medals.append(medal)

        return medals

    def missing_medals(self):
        """Gets the names of all the medals that aren't yet on the DB"""
        current_medals = set(DBWrapper.find_all('Medals', ['name']))
        total_medals = set(self.get_medal_names())

        return list(total_medals - current_medals)
