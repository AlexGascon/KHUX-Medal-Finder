import unittest
import json
import peewee
from unittest.mock import patch

from khux_medal_finder.models import BaseModel, Medal, MedalFactory

test_db = peewee.SqliteDatabase(':memory:')
MODELS = [BaseModel, Medal]

class BaseDBTestCase(unittest.TestCase):
    """TestCase class to use in the test cases where we need to query a DB.
    It uses a temporary DB to avoid messing with our production one"""

    def setUp(self):

        # Bind model classes to test db
        for model in MODELS:
            model.bind(test_db, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

        super(BaseDBTestCase, self).setUp()

    def tearDown(self):
        # Not strictly necessary since in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

        super(BaseDBTestCase, self).tearDown()

class TestModels(BaseDBTestCase):
    """Tests for the different ORM models"""

    """BaseModel model"""
    def test_base_model_has_database(self):
        self.assertIsNotNone(BaseModel._meta.database)

    """Medal model"""
    def test_medal_model_has_correct_fields(self):
        expected_fields = ['cost', 'defence', 'direction', 'element', 'hits',
                           'medal_id', 'image_link', 'multiplier_min', 'multiplier_max',
                           'name', 'notes', 'pullable', 'rarity', 'region',
                           'strength', 'targets', 'tier', 'type', 'voice_link']
        self.assertCountEqual(Medal._meta.sorted_field_names, expected_fields)

    def test_medal_model_fields_have_correct_types(self):
        fields = Medal._meta.fields
        self.assertIsInstance(fields['cost'], peewee.IntegerField)
        self.assertIsInstance(fields['defence'], peewee.IntegerField)
        self.assertIsInstance(fields['direction'], peewee.CharField)
        self.assertIsInstance(fields['element'], peewee.CharField)
        self.assertIsInstance(fields['hits'], peewee.IntegerField)
        self.assertIsInstance(fields['image_link'], peewee.TextField)
        self.assertIsInstance(fields['medal_id'], peewee.IntegerField)
        self.assertIsInstance(fields['multiplier_min'], peewee.FloatField)
        self.assertIsInstance(fields['multiplier_max'], peewee.FloatField)
        self.assertIsInstance(fields['name'], peewee.TextField)
        self.assertIsInstance(fields['notes'], peewee.TextField)
        self.assertIsInstance(fields['pullable'], peewee.CharField)
        self.assertIsInstance(fields['rarity'], peewee.IntegerField)
        self.assertIsInstance(fields['region'], peewee.CharField)
        self.assertIsInstance(fields['strength'], peewee.IntegerField)
        self.assertIsInstance(fields['targets'], peewee.CharField)
        self.assertIsInstance(fields['tier'], peewee.IntegerField)
        self.assertIsInstance(fields['type'], peewee.CharField)
        self.assertIsInstance(fields['voice_link'], peewee.TextField)

class TestMedalFactory(BaseDBTestCase):

    # We override the run method of the Test class to have a simpler way of mocking
    # all the tests
    def run(self, result=None):
        with patch.object(Medal, 'save', return_value=1):
            super(TestMedalFactory, self).run(result)

    def setUp(self):
        super(TestMedalFactory, self).setUp()

        with open('test/fixtures/models/combat_medal_data.json') as fixture:
            self.combat_medal_json = json.loads(fixture.read())

        with open('test/fixtures/models/combat_medal_with_ranged_multiplier_data.json') as fixture:
            self.combat_medal_ranged_multiplier_json = json.loads(fixture.read())

        with open('test/fixtures/models/non_combat_medal_data.json') as fixture:
            self.non_combat_medal_json = json.loads(fixture.read())

        self.combat_medal = MedalFactory.medal(self.combat_medal_json)
        self.combat_medal_ranged_multiplier = MedalFactory.medal(self.combat_medal_ranged_multiplier_json)

    def test_creates_medal_if_all_fields_are_present(self):
        self.assertIsInstance(self.combat_medal, Medal)

    def test_doesnt_create_medal_if_type_is_not_combat(self):
        self.assertIsNone(MedalFactory.medal(self.non_combat_medal_json))

    def test_sets_fields_correctly_in_medal(self):
        self.assertEqual(self.combat_medal.medal_id, 862)
        self.assertEqual(self.combat_medal.cost, 2)
        self.assertEqual(self.combat_medal.defence, 5618)
        self.assertEqual(self.combat_medal.direction, "Upright")
        self.assertEqual(self.combat_medal.element, "Speed")
        self.assertEqual(self.combat_medal.hits, 13)
        self.assertEqual(self.combat_medal.image_link, "/static/medal_images//KH_02_Terra_and_Ventus_6.png")
        self.assertEqual(self.combat_medal.name, "KH0.2 Terra & Ventus")
        self.assertEqual(self.combat_medal.notes, "Raises your power and speed attack by two steps for two turns; deals large damage")
        self.assertEqual(self.combat_medal.pullable, "No")
        self.assertEqual(self.combat_medal.rarity, 6)
        self.assertEqual(self.combat_medal.region, "na")
        self.assertEqual(self.combat_medal.strength, 5696)
        self.assertEqual(self.combat_medal.targets, "Single")
        self.assertEqual(self.combat_medal.tier, 5)
        self.assertEqual(self.combat_medal.type, "Combat")
        self.assertEqual(self.combat_medal.voice_link, "/some/random/uri/path.mp3")

    def test_parses_multiplier_correctly_if_medal_has_single_multiplier(self):
        self.assertEqual(self.combat_medal.multiplier_min, 3.40)
        self.assertEqual(self.combat_medal.multiplier_max, 3.40)

    def test_parses_multiplier_correctly_if_medal_has_ranged_multiplier(self):
        self.assertEqual(self.combat_medal_ranged_multiplier.multiplier_min, 2.61)
        self.assertEqual(self.combat_medal_ranged_multiplier.multiplier_max, 3.85)

    def test_doesnt_create_medal_if_the_json_contains_an_error(self):
        json_with_error = {"error": "Error message to use in this test"}
        self.assertIsNone(MedalFactory.medal(json_with_error))

    def test_doesnt_create_medal_if_cost_is_missing(self):
        combat_medal_json_faulty = self.combat_medal_json
        combat_medal_json_faulty.pop('cost')

        created_medal = MedalFactory.medal(combat_medal_json_faulty)
        self.assertIsNone(created_medal)

    def test_doesnt_create_medal_if_direction_is_missing(self):
        combat_medal_json_faulty = self.combat_medal_json.copy()
        combat_medal_json_faulty.pop('direction')

        created_medal = MedalFactory.medal(combat_medal_json_faulty)
        self.assertIsNone(created_medal)

    def test_doesnt_create_medal_if_element_is_missing(self):
        combat_medal_json_faulty = self.combat_medal_json.copy()
        combat_medal_json_faulty.pop('element')

        created_medal = MedalFactory.medal(combat_medal_json_faulty)
        self.assertIsNone(created_medal)

    def test_doesnt_create_medal_if_hits_is_missing(self):
        combat_medal_json_faulty = self.combat_medal_json.copy()
        combat_medal_json_faulty.pop('hits')

        created_medal = MedalFactory.medal(combat_medal_json_faulty)
        self.assertIsNone(created_medal)

    def test_doesnt_create_medal_if_id_is_missing(self):
        combat_medal_json_faulty = self.combat_medal_json.copy()
        combat_medal_json_faulty.pop('id')

        created_medal = MedalFactory.medal(combat_medal_json_faulty)
        self.assertIsNone(created_medal)

    def test_doesnt_create_medal_if_multiplier_is_missing(self):
        combat_medal_json_faulty = self.combat_medal_json.copy()
        combat_medal_json_faulty.pop('multiplier')

        created_medal = MedalFactory.medal(combat_medal_json_faulty)
        self.assertIsNone(created_medal)

    def test_doesnt_create_medal_if_name_is_missing(self):
        combat_medal_json_faulty = self.combat_medal_json.copy()
        combat_medal_json_faulty.pop('name')

        created_medal = MedalFactory.medal(combat_medal_json_faulty)
        self.assertIsNone(created_medal)

    def test_doesnt_create_medal_if_rarity_is_missing(self):
        combat_medal_json_faulty = self.combat_medal_json.copy()
        combat_medal_json_faulty.pop('rarity')

        created_medal = MedalFactory.medal(combat_medal_json_faulty)
        self.assertIsNone(created_medal)

    def test_doesnt_create_medal_if_targets_is_missing(self):
        combat_medal_json_faulty = self.combat_medal_json.copy()
        combat_medal_json_faulty.pop('targets')

        created_medal = MedalFactory.medal(combat_medal_json_faulty)
        self.assertIsNone(created_medal)

    def test_doesnt_create_medal_if_tier_is_missing(self):
        combat_medal_json_faulty = self.combat_medal_json.copy()
        combat_medal_json_faulty.pop('tier')

        created_medal = MedalFactory.medal(combat_medal_json_faulty)
        self.assertIsNone(created_medal)

    def test_doesnt_create_medal_if_type_is_missing(self):
        combat_medal_json_faulty = self.combat_medal_json.copy()
        combat_medal_json_faulty.pop('type')

        created_medal = MedalFactory.medal(combat_medal_json_faulty)
        self.assertIsNone(created_medal)

    def test_creates_medal_if_any_other_field_is_missing(self):
        combat_medal_json_faulty = self.combat_medal_json.copy()
        combat_medal_json_faulty.pop('defence')
        combat_medal_json_faulty.pop('image_link')
        combat_medal_json_faulty.pop('notes')
        combat_medal_json_faulty.pop('pullable')
        combat_medal_json_faulty.pop('region')
        combat_medal_json_faulty.pop('strength')
        combat_medal_json_faulty.pop('voice_link')

        created_medal = MedalFactory.medal(combat_medal_json_faulty)
        self.assertIsInstance(created_medal, Medal)
