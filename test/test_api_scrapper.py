import unittest
import json
import requests_mock
from unittest.mock import patch

from khux_medal_finder.api import Scrapper
from khux_medal_finder.models import Medal
from khux_medal_finder.factories import MedalFactory

from test.helpers import BaseDBTestCase

class TestScrapper(BaseDBTestCase):

    def setUp(self):
        self.scrapper = Scrapper()

        # Saving the requests_mock as an object to reuse it in the class
        with requests_mock.Mocker() as mock:
            self.requests_mock = mock

            # Mocking all the URLs we'll use on this test class
            names_endpoint = 'https://www.khuxbot.com/api/v1/medal?q=names'
            names_fixture_file = 'test/fixtures/scrapper/medal_names.json'
            with open(names_fixture_file) as names_fixture:
                names_response = json.loads(names_fixture.read())
            self.requests_mock.get(names_endpoint, json=names_response)

            medal_data_endpoint = 'https://www.khuxbot.com/api/v1/medal?q=data&medal=illustrated%20halloween%20goofy'
            medal_data_fixture_file = 'test/fixtures/scrapper/medal_data.json'
            with open(medal_data_fixture_file) as medal_data_fixture:
                medal_data_response = json.loads(medal_data_fixture.read())
            self.requests_mock.get(medal_data_endpoint, json=medal_data_response)
            
            medals_data_endpoint = 'https://www.khuxbot.com/api/v1/medal?q=data&medal=axel%20b'
            medals_data_fixture_file = 'test/fixtures/scrapper/medals_data.json'
            with open(medals_data_fixture_file) as medals_data_fixture:
                medals_data_response = json.loads(medals_data_fixture.read())
            self.requests_mock.get(medals_data_endpoint, json=medals_data_response)

            medal_not_exist_data_endpoint = 'https://www.khuxbot.com/api/v1/medal?q=data&medal=Illustrated%20Pence%20HD'
            self.requests_mock.get(medal_not_exist_data_endpoint, json={"error": "No medal found"})
            
            medal_with_symbol_in_name_endpoint_1 = 'https://www.khuxbot.com/api/v1/medal?q=data&medal=kh0.2%20terra%20%26%20ventus'
            medal_with_symbol_in_name_fixture_file_1 = 'test/fixtures/scrapper/medal_with_symbol_in_name_1.json'
            with open(medal_with_symbol_in_name_fixture_file_1) as medal_with_symbol_in_name_fixture_1:
                medal_with_symbol_in_name_response_1 = json.loads(medal_with_symbol_in_name_fixture_1.read())
            self.requests_mock.get(medal_with_symbol_in_name_endpoint_1, json=medal_with_symbol_in_name_response_1)
            
            medal_with_symbol_in_name_endpoint_2 = 'https://www.khuxbot.com/api/v1/medal?q=data&medal=key%20art%20%233'
            medal_with_symbol_in_name_fixture_file_2 = 'test/fixtures/scrapper/medal_with_symbol_in_name_2.json'
            with open(medal_with_symbol_in_name_fixture_file_2) as medal_with_symbol_in_name_fixture_2:
                medal_with_symbol_in_name_response_2 = json.loads(medal_with_symbol_in_name_fixture_2.read())
            self.requests_mock.get(medal_with_symbol_in_name_endpoint_2, json=medal_with_symbol_in_name_response_2)
            
            medal_with_symbol_in_name_endpoint_3 = 'https://www.khuxbot.com/api/v1/medal?q=data&medal=HD%20Invi%20%5BEX%5D'
            medal_with_symbol_in_name_fixture_file_3 = 'test/fixtures/scrapper/medal_with_symbol_in_name_3.json'
            with open(medal_with_symbol_in_name_fixture_file_3) as medal_with_symbol_in_name_fixture_3:
                medal_with_symbol_in_name_response_3 = json.loads(medal_with_symbol_in_name_fixture_3.read())
            self.requests_mock.get(medal_with_symbol_in_name_endpoint_3, json=medal_with_symbol_in_name_response_3)

        super(TestScrapper, self).setUp()

    def test_get_medals_when_one_medal_exists(self):
        expected_medals = [{"cost": 7, "defence": 5645, "direction": "Upright", "element": "Power", "hits": 3,  "id": 1051, "image_link": "/static/medal_images//Illustrated_Halloween_Goofy_6.png", "multiplier": "x4.13", "name": "Illustrated Halloween Goofy", "notes": "Restores 3 guates", "pullable": "No", "rarity": 6, "region": "na", "strength": 5759, "targets": "All", "tier": 7, "type": "Combat", "voice_link": None}]

        with self.requests_mock:
            medals = self.scrapper.get_medals('illustrated halloween goofy')

        self.assertCountEqual(medals, expected_medals)

    def test_get_medals_when_several_medals_exist(self):
        expected_medals = [
            {"cost": 1, "defence": 4274, "direction": "Reversed", "element": "Power", "hits": 6, "id": 986, "image_link": "/static/medal_images//Axel_B_5.png", "multiplier": "x1.72-3.20", "name": "Axel B", "notes": "Increases your power attack by three steps for one turn; deals more damage the further forward it's set in your deck", "pullable": "No", "rarity": 5, "region": "na", "strength": 4377, "targets": "Random", "tier": 3, "type": "Combat", "voice_link": None},
            {"cost": 1, "defence": 5512, "direction": "Reversed", "element": "Power", "hits": 6, "id": 987, "image_link": "/static/medal_images//Axel_B_6.png", "multiplier": "x1.78-3.26", "name": "Axel B", "notes": "Increases your power attack by three steps for one turn; deals more damage the further forward it's set in your deck", "pullable": "No", "rarity": 6, "region": "na", "strength": 5645, "targets": "Random", "tier": 3, "type": "Combat", "voice_link": None}
        ]

        with self.requests_mock:
            medals = self.scrapper.get_medals('axel b')

        self.assertCountEqual(medals, expected_medals)

    def test_get_medals_when_medal_doesnt_exist(self):
        with self.requests_mock:
            medals = self.scrapper.get_medals('Illustrated Pence HD')

        self.assertCountEqual(medals, [])

    def test_get_medals_when_there_are_symbols_in_query(self):
        expected_medals_1 = [{"cost": 2, "defence": 5618, "direction": "Upright", "element": "Speed", "hits": 13, "id": 862, "image_link": "/static/medal_images//KH_02_Terra_and_Ventus_6.png", "multiplier": "x3.40", "name": "KH0.2 Terra & Ventus", "notes": "Raises your power and speed attack by two steps for two turns; deals large damage", "pullable": "No", "rarity": 6, "region": "na", "strength": 5696, "targets": "Single", "tier": 5, "type": "Combat", "voice_link": None}]
        expected_medals_2 = [{"cost": 2, "defence": 5590, "direction": "Reversed", "element": "Speed", "hits": 5, "id": 637, "image_link": "/static/medal_images//Key_Art_3_6.png", "multiplier": "x1.38-2.72", "name": "Key Art #3", "notes": "Decreases enemy defense by one stage for the remainder of the turn; deals more damage the greater your HP", "pullable": "Yes", "rarity": 6, "region": "na", "strength": 5677, "targets": "All", "tier": 5, "type": "Combat", "voice_link": None}]
        expected_medals_3 = [{"cost": 1, "defence": 5861, "direction": "Upright", "element": "Magic", "hits": 4, "id": 1014, "image_link": "/static/medal_images//HD_Invi_EX_6.png", "multiplier": "x3.12-4.32", "name": "HD Invi [EX]", "notes": "Increases your magic attack by seven steps, decreases enemy general defense by two steps and enemy magic defense by seven steps for two turns; deals more damage when only one enemy in the group remains or all raid parts have been destroyed; doesn't affect enemy counters", "pullable": "No", "rarity": 6, "region": "na", "strength": 6030, "targets": "All", "tier": 7, "type": "Combat", "voice_link": None}]

        with self.requests_mock:
            medals_1 = self.scrapper.get_medals('KH0.2 Terra & Ventus')
            medals_2 = self.scrapper.get_medals('Key Art #3')
            medals_3 = self.scrapper.get_medals('HD Invi [EX]')

        self.assertCountEqual(medals_1, expected_medals_1)
        self.assertCountEqual(medals_2, expected_medals_2)
        self.assertCountEqual(medals_3, expected_medals_3)

    def test_get_medal_names(self):
        expected_names_file = 'test/fixtures/scrapper/medal_names.txt'
        with open(expected_names_file) as content:
            expected_names = [name.strip() for name in content.readlines()]

        with self.requests_mock:
            self.assertCountEqual(self.scrapper.get_medal_names(), expected_names)

    @patch.object(Medal, 'select', create=True)
    def test_missing_medals_when_there_are_missing_medals(self, mock_select):
        all_medals_file = 'test/fixtures/scrapper/medal_names.txt'
        with open(all_medals_file) as content:
            medals = [Medal(name=name.strip()) for name in content.readlines()]
            mock_select.return_value = medals[:-3]

        expected_missing_medals = ['hd invi [ex]', 'axel b', 'illustrated halloween goofy']
        with self.requests_mock:
            missing_medals = self.scrapper.missing_medals()

        self.assertCountEqual(expected_missing_medals, missing_medals)
        mock_select.assert_called_once()

    @patch.object(Medal, 'select', create=True)
    def test_missing_medals_when_there_arent_missing_medals(self, mock_select):
        all_medals_file = 'test/fixtures/scrapper/medal_names.txt'
        with open(all_medals_file) as content:
            medals = [Medal(name=name.strip()) for name in content.readlines()]
            mock_select.return_value = medals

        with self.requests_mock:
            missing_medals = self.scrapper.missing_medals()

        self.assertCountEqual(missing_medals, [])
        mock_select.assert_called_once()

    @patch.object(Scrapper, 'get_medal_names')
    def test_missing_medals_stop_being_missing_when_we_create_them(self, mock_get_medal_names):
        medal_names = ['hd invi [ex]', 'axel b', 'illustrated halloween goofy']
        mock_get_medal_names.return_value = medal_names

        number_of_missing_medals = len(self.scrapper.missing_medals())
        invi_data_filename = 'test/fixtures/scrapper/medal_with_symbol_in_name_3.json'
        with open(invi_data_filename) as invi_data_file:
            invi_data = json.loads(invi_data_file.read())['medal']['0']
            MedalFactory.medal(invi_data)

        self.assertEqual(len(self.scrapper.missing_medals()), number_of_missing_medals - 1)

    @patch.object(Medal, 'get_or_none', return_value=None)
    @patch.object(Scrapper, 'missing_medals')
    def test_scrape_missing_medals_when_medals_are_not_in_DB(self, mock_missing_medals, mock_get_or_none):
        missing_medals = ['hd invi [ex]', 'axel b', 'illustrated halloween goofy']
        mock_missing_medals.return_value = missing_medals

        with patch.object(MedalFactory, 'medal') as mocked_medalfactory:
            with self.requests_mock:
                self.scrapper.scrape_missing_medals()

            # Despite there are only 3 medals in missing_medals, the method is
            # called 4 times because Axel B has two versions: 5 and 6 stars.
            self.assertEqual(mocked_medalfactory.call_count, 4)

    @patch.object(Medal, 'get_or_none', return_value=True)
    @patch.object(Scrapper, 'missing_medals')
    def test_scrape_missing_medals_when_medals_are_in_DB(self, mock_missing_medals, mock_get_or_none):
        mock_missing_medals.return_value = ['hd invi [ex]', 'axel b', 'illustrated halloween goofy']

        with patch.object(MedalFactory, 'medal') as mocked_medalfactory:
            with self.requests_mock:
                self.scrapper.scrape_missing_medals()

            mocked_medalfactory.assert_not_called()
