import requests

BASE_ENDPOINT = "http://www.khuxbot.com/api/v1/medal?q=data&"


def compose_endpoint(filters):
    """Given a dictionary with the filters to use in the search, composes the endpoint URL"""

    # We'll only search for Level 6 medals, as those are the ones used in setups
    base_filter = 'filter={"rarity": 6'

    for filter_name in filters:
        base_filter += f",\"{filter_name}\":\"{filters[filter_name]}\""

    base_filter += '}'

    return BASE_ENDPOINT + base_filter


def get_medals(filters):
    """Given the filters to search, returns a list with a dict representing each medal"""
    endpoint = compose_endpoint(filters)
    server_response = requests.get(endpoint)

    medals = server_response.json()['medal']

    # Returning the medals as a list instead of a dict, as it's easier to work with it
    return [medals[key_id] for key_id in medals]


def combine_searches(filters_list):
    """Given a list containing sets of filters, executes the necessary searches
    and combines the results"""
    medals = []

    for filters in filters_list:
        medals += get_medals(filters)

    return medals
