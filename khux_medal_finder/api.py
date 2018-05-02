import requests
from urllib.parse import urlencode

from khux_medal_finder.models import Medal, MedalFactory

class Search:

    def __init__(self):
        self.BASE_ENDPOINT = "http://www.khuxbot.com/api/v1/medal?q=data&"

    def endpoint(self, filters):
        """Given a dictionary with the filters to use in the search, composes the endpoint URL"""

        # We'll only search for Level 6 medals, as those are the ones used in setups
        base_filter = 'filter={"rarity": 6'

        for filter_name in filters:
            base_filter += f",\"{filter_name}\":\"{filters[filter_name]}\""

        base_filter += '}'

        return self.BASE_ENDPOINT + base_filter

    def medals(self, filters):
        """Given the filters to search, returns a list with a dict representing each medal"""
        endpoint = self.endpoint(filters)
        server_response = requests.get(endpoint)

        medals = server_response.json()['medal']

        # Returning the medals as a list instead of a dict, as it's easier to work with it
        return [medals[key_id] for key_id in medals]

    def combine_searches(self, filters_list):
        """Given a list containing sets of filters, executes the necessary searches
        and combines the results"""
        medals = []

        for filters in filters_list:
            medals += self.medals(filters)

        return medals


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
            medals.append(medal)#MedalFactory.medal(medal))

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
                    if not Medal.get_or_none(Medal.id == medal['id']):
                        print(f"Creating medal {medal['name'] - medal['rarity']}")
                        success = (MedalFactory.medal(medal) and success)

        except Exception as e:
            success = False

        finally:
           return success