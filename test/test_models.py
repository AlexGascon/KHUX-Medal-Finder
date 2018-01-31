import unittest

from src.models import *


class TestModels(unittest.TestCase):

    def test_base_model_has_database(self):
        self.assertIn('database', BaseModel.fields)