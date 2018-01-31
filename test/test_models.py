import unittest

from src.models import *


class TestModels(unittest.TestCase):

    def test_base_model_has_database(self):
        self.assertIsNotNone(BaseModel._meta.database)

    def test_base_model_has_correct_database(self):
        self.assertIsInstance(BaseModel._meta.database, PostgresqlDatabase)

    def test_medal_model_has_correct_database(self):
        self.assertIsInstance(Medal._meta.database, PostgresqlDatabase)
