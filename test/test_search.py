import unittest
import requests_mock

import json
from src.search import *


class TestSearch(unittest.TestCase):

    def test_compose_endpoint(self):
        filters = {"direction": "Upright", "element": "Power", "cost": 4}
        expected_endpoint = 'http://www.khuxbot.com/api/v1/medal?q=data&filter={"rarity": 6,"direction":"Upright","element":"Power","cost":"4"}'

        self.assertEqual(expected_endpoint, compose_endpoint(filters))

    @requests_mock.Mocker()
    def test_get_medals(self, mock_requests):
        # Mocking HTTP requests to avoid making real requests
        api_url = 'http://www.khuxbot.com/api/v1/medal?q=data&filter=%7B%22rarity%22:%206,%22direction%22:%22Upright%22,%22element%22:%22Power%22,%22cost%22:%224%22,%22tier%22:%226%22%7D'
        with open('test/fixtures/medals_upright_power_c4_t6.json') as fixture:
            api_response = json.loads(fixture.read())
        mock_requests.get(api_url, json=api_response)

        filters = {"direction": "Upright", "element": "Power", "cost": 4, "tier": 6}
        expected_medals = [
            {"cost": 4, "defence": 5665, "direction": "Upright", "element": "Power", "hits": 12, "id": 943, "image_link": "/static/medal_images//Kings_Roar_6.png", "multiplier": "x2.10-3.28", "name": "Kings Roar", "notes": "Decreases enemy defense by one step for two turns; increases your power attack by two steps for two turns; deals more damage the further back it's set in your deck", "pullable": "Yes", "rarity": 6, "region": "na", "strength": 5753, "targets": "All", "tier": 6, "type": "Combat"},
            {"cost": 4, "defence": 5718, "direction": "Upright", "element": "Power", "hits": 11, "id": 982, "image_link": "/static/medal_images//Toon_Sora_6.png", "multiplier": "x1.99-3.35","name": "Toon Sora","notes": "Increases the enemy's count by +1, increases your PSM attack by three steps for two turns, deals more damage the higher your HP","pullable": "No","rarity": 6,"region": "na","strength": 5756,"targets": "All","tier": 6,"type": "Combat"}
        ]

        self.assertListEqual(expected_medals, get_medals(filters))

if __name__ == '__main__':
    unittest.main()