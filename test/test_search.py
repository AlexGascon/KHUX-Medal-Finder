import unittest
from src.search import *


class TestSearch(unittest.TestCase):

    def test_compose_endpoint(self):
        filters = {"direction": "Upright", "element": "Power", "cost": 4}
        expected_endpoint = 'http://www.khuxbot.com/api/v1/medal?q=data&filter={"rarity": 6,"direction":"Upright","element":"Power","cost":"4"}'

        self.assertEqual(expected_endpoint, compose_endpoint(filters))

    def test_get_medals(self):
        filters = {"direction": "Upright", "element": "Power", "cost": 4, "tier": 6}
        expected_medals = [
            { "cost": 4, "defence": 5665, "direction": "Upright", "element": "Power", "hits": 12, "id": 943, "image_link": "/static/medal_images//Kings_Roar_6.png", "multiplier": "x2.10-3.28", "name": "Kings Roar", "notes": "Decreases enemy defense by one step for two turns; increases your power attack by two steps for two turns; deals more damage the further back it's set in your deck", "pullable": "Yes", "rarity": 6, "region": "na", "strength": 5753, "targets": "All", "tier": 6, "type": "Combat" },
            { "cost": 4, "defence": 5718, "direction": "Upright", "element": "Power", "hits": 11, "id": 982, "image_link": "/static/medal_images//Toon_Sora_6.png", "multiplier": "x1.99-3.35","name": "Toon Sora","notes": "Increases the enemy's count by +1, increases your PSM attack by three steps for two turns, deals more damage the higher your HP","pullable": "No","rarity": 6,"region": "na","strength": 5756,"targets": "All","tier": 6,"type": "Combat" }
        ]

        self.assertListEqual(expected_medals, get_medals(filters))

if __name__ == '__main__':
    unittest.main()