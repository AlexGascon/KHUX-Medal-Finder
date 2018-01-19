import requests

class Scrapper:

    def __init__(self):
        self.names_endpoint = 'https://www.khuxbot.com/api/v1/medal?q=names'

    def get_medal_names(self):
        response = requests.get(self.names_endpoint)
        return (response.json())['names']