import requests

from src.db import DBWrapper


class Scrapper:

    def __init__(self):
        self.names_endpoint = 'https://www.khuxbot.com/api/v1/medal?q=names'

    def get_medal_names(self):
        response = requests.get(self.names_endpoint)
        return (response.json())['names']

    def missing_medals(self):
        """Gets the names of all the medals that aren't yet on the DB"""
        current_medals = set(DBWrapper.find_all('Medals', ['name']))
        total_medals = set(self.get_medal_names())

        return list(total_medals - current_medals)