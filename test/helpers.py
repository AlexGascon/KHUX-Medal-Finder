import unittest
import peewee
from khux_medal_finder.models import BaseModel, Medal, Comment, Reply

test_db = peewee.SqliteDatabase(':memory:')
MODELS = [BaseModel, Medal, Comment, Reply]

class BaseDBTestCase(unittest.TestCase):
    """TestCase class to use in the test cases where we need to query a DB.
    It uses a temporary DB to avoid messing with our production one"""
    def run(self, result=None):
       with test_db.bind_ctx(MODELS):
           super(BaseDBTestCase, self).run(result)

    def setUp(self):
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

