import unittest
import peewee

from src.models import *


class TestModels(unittest.TestCase):
    "Tests for the different ORM models"

    """BaseModel model"""
    def test_base_model_has_database(self):
        self.assertIsNotNone(BaseModel._meta.database)

    def test_base_model_has_correct_database(self):
        self.assertIsInstance(BaseModel._meta.database, PostgresqlDatabase)

    """Medal model"""
    def test_medal_model_has_correct_database(self):
        self.assertIsInstance(Medal._meta.database, PostgresqlDatabase)

    def test_medal_model_has_correct_fields(self):
        expected_fields = ['cost', 'defence', 'direction', 'hits', 'id',
                           'image_link', 'multiplier_min', 'multiplier_max',
                           'name', 'notes', 'pullable', 'rarity', 'region',
                           'strength', 'targets', 'tier', 'type', 'voice_link']
        self.assertCountEqual(Medal._meta.sorted_field_names, expected_fields)

    def test_medal_model_fields_have_correct_types(self):
        fields = Medal._meta.fields
        self.assertEqual(type(fields['cost']), peewee.IntegerField)
        self.assertEqual(type(fields['defence']), peewee.IntegerField)
        self.assertEqual(type(fields['direction']), peewee.CharField)
        self.assertEqual(type(fields['hits']), peewee.IntegerField)
        self.assertEqual(type(fields['id']), peewee.IntegerField)
        self.assertEqual(type(fields['image_link']), peewee.TextField)
        self.assertEqual(type(fields['multiplier_min']), peewee.FloatField)
        self.assertEqual(type(fields['multiplier_max']), peewee.FloatField)
        self.assertEqual(type(fields['name']), peewee.TextField)
        self.assertEqual(type(fields['notes']), peewee.TextField)
        self.assertEqual(type(fields['pullable']), peewee.CharField)
        self.assertEqual(type(fields['rarity']), peewee.IntegerField)
        self.assertEqual(type(fields['region']), peewee.CharField)
        self.assertEqual(type(fields['strength']), peewee.IntegerField)
        self.assertEqual(type(fields['targets']), peewee.CharField)
        self.assertEqual(type(fields['tier']), peewee.IntegerField)
        self.assertEqual(type(fields['type']), peewee.CharField)
        self.assertEqual(type(fields['voice_link']), peewee.TextField)

