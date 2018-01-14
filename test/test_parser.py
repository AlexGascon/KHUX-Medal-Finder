import unittest

from src.parser import extract_filters

class TestExtractFilters(unittest.TestCase):

    def setUp(self):
        # Direction
        self.comment_upright = "Foo bar baz Upright baz bar foo"
        self.comment_reversed = "Lorem impsum Reversed medal ipsum"
        # Elements
        self.comment_power = "Lorem impsum Power medal ipsum"
        self.comment_speed = "Lorem impsum Speed medal ipsum"
        self.comment_magic = "Lorem impsum Magic medal ipsum"
        self.comment_power_magic = "Lorem impsum Power medal ipsum Magic baz bar foo"
        self.comment_speed_power = "Lorem impsum Speed medal ipsum Power baz bar foo"
        # Targets
        self.comment_single = "Lorem impsum Single medal ipsum"
        self.comment_aoe = "Lorem impsum AoE medal ipsum"
        self.comment_random = "Lorem impsum Random medal ipsum"
        self.comment_single_aoe = "Lorem impsum Single medal ipsum AoE baz bar foo"
        self.comment_single_random = "Lorem impsum Single medal ipsum Random baz bar foo"


    def test_direction_filters_work(self):
        expected_upright_filter = {"direction": "Upright"}
        expected_reversed_filter = {"direction": "Reversed"}
        
        self.assertDictEqual(extract_filters(self.comment_upright), expected_upright_filter)
        self.assertDictEqual(extract_filters(self.comment_reversed), expected_reversed_filter)
        
    def test_element_filters_work(self):
        expected_power_filter = {"element": "Power"}
        expected_speed_filter = {"element": "Speed"}
        expected_magic_filter = {"element": "Magic"}
        expected_power_magic_filter = {"element": ["Power", "Magic"]}
        expected_speed_power_filter = {"element": ["Power", "Speed"]}
        
        self.assertDictEqual(extract_filters(self.comment_power), expected_power_filter)
        self.assertDictEqual(extract_filters(self.comment_speed), expected_speed_filter)
        self.assertDictEqual(extract_filters(self.comment_magic), expected_magic_filter)
        self.assertDictEqual(extract_filters(self.comment_power_magic), expected_power_magic_filter)
        self.assertDictEqual(extract_filters(self.comment_speed_power), expected_speed_power_filter)
        
    def test_target_filters_work(self):
        expected_single_filter = {"targets": "Single"}
        expected_aoe_filter = {"targets": "All"}
        expected_random_filter = {"targets": "Random"}
        expected_single_aoe_filter = {"targets": ["Single", "All"]}
        expected_single_random_filter = {"targets": ["Single", "Random"]}
        
        self.assertDictEqual(extract_filters(self.comment_single), expected_single_filter)
        self.assertDictEqual(extract_filters(self.comment_aoe), expected_aoe_filter)
        self.assertDictEqual(extract_filters(self.comment_random), expected_random_filter)
        self.assertDictEqual(extract_filters(self.comment_single_aoe), expected_single_aoe_filter)
        self.assertDictEqual(extract_filters(self.comment_single_random), expected_single_random_filter)

        

