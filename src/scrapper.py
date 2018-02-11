import requests
from urllib.parse import urlencode

from src.db import DBWrapper
from src.models import Medal


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
        for _, medal in medals_dict.items():
            medals.append(medal)

        return medals

    def missing_medals(self):
        """Gets the names of all the medals that aren't yet on the DB"""
        current_medals = set(medal.name for medal in Medal.select())
        total_medals = set(self.get_medal_names())

        return list(total_medals - current_medals)

    def scrape_missing_medals(self):
        """Saves in the DB the medals that aren't there yet"""
        success = True

        try:
            missing_medals = self.missing_medals()

            for medal_name in missing_medals:
                matching_medals = self.get_medals(medal_name)

                for medal in matching_medals:
                    if not DBWrapper.is_present('Medals', {"id": medal['id']}):
                        success = (DBWrapper.save('Medals', medal) and success)

        except Exception:
            success = False

        finally:
            return success