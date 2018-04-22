import json
import unittest
import peewee

from khux_medal_finder.models import MedalFactory, Medal
from khux_medal_finder.helpers import prepare_reply_body

test_db = peewee.SqliteDatabase(':memory:')
class TestPrepareReplyBody(unittest.TestCase):
    def setUp(self):
        Medal.bind(test_db, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables([Medal])

        with open('test/fixtures/models/combat_medal_data.json') as fixture:
            combat_medal_json = json.loads(fixture.read())
            self.combat_medal = MedalFactory.medal(combat_medal_json)

        with open('test/fixtures/models/combat_medal_with_ranged_multiplier_data.json') as fixture:
            combat_medal_ranged_multiplier_json = json.loads(fixture.read())
            self.combat_medal_ranged_multiplier = MedalFactory.medal(combat_medal_ranged_multiplier_json)

    def tearDown(self):
        # Not strictly necessary since in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(Medal)
        # Close connection to db.
        test_db.close()

    def test_if_there_are_no_medals_raises_exception(self):
        with self.assertRaises(ValueError):
            prepare_reply_body([])

    def test_if_there_is_only_one_medal_generates_the_table_correctly(self):
        expected_table = "Medal|Direction|Element|Targets|Multiplier|Tier|Hits|Notes\n" +\
                         ":--|:--|:--|:--|:--|:--|:--|:--|\n" + \
                         "KH0.2 Terra & Ventus|Upright|Speed|Single|x3.4|5|13|Raises your power and speed attack by two steps for two turns; deals large damage"
        obtained_table = prepare_reply_body([self.combat_medal])

        self.assertEqual(obtained_table, expected_table)

    def test_if_there_are_several_medals_generates_the_table_correctly(self):
        expected_table = "Medal|Direction|Element|Targets|Multiplier|Tier|Hits|Notes\n" +\
                         ":--|:--|:--|:--|:--|:--|:--|:--|\n" + \
                         "KH0.2 Terra & Ventus|Upright|Speed|Single|x3.4|5|13|Raises your power and speed attack by two steps for two turns; deals large damage\n" + \
                         "Final Boss Xion|Reversed|Speed|All|x2.61 - 3.85|6|1|Decreases enemy defense by two steps for two turns; deals more damage the more ability gauges you have remaining"
        obtained_table = prepare_reply_body([self.combat_medal, self.combat_medal_ranged_multiplier])
        self.assertEqual(obtained_table, expected_table)

    def test_the_amount_of_medals_shown_is_correctly_limited(self):
        expected_table = "Medal|Direction|Element|Targets|Multiplier|Tier|Hits|Notes\n" + \
                         ":--|:--|:--|:--|:--|:--|:--|:--|\n" + \
                         "KH0.2 Terra & Ventus|Upright|Speed|Single|x3.4|5|13|Raises your power and speed attack by two steps for two turns; deals large damage\n" + \
                         "KH0.2 Terra & Ventus|Upright|Speed|Single|x3.4|5|13|Raises your power and speed attack by two steps for two turns; deals large damage\n" + \
                         "KH0.2 Terra & Ventus|Upright|Speed|Single|x3.4|5|13|Raises your power and speed attack by two steps for two turns; deals large damage\n" + \
                         "KH0.2 Terra & Ventus|Upright|Speed|Single|x3.4|5|13|Raises your power and speed attack by two steps for two turns; deals large damage\n" + \
                         "KH0.2 Terra & Ventus|Upright|Speed|Single|x3.4|5|13|Raises your power and speed attack by two steps for two turns; deals large damage\n" + \
                         "KH0.2 Terra & Ventus|Upright|Speed|Single|x3.4|5|13|Raises your power and speed attack by two steps for two turns; deals large damage\n" + \
                         "KH0.2 Terra & Ventus|Upright|Speed|Single|x3.4|5|13|Raises your power and speed attack by two steps for two turns; deals large damage\n" + \
                         "KH0.2 Terra & Ventus|Upright|Speed|Single|x3.4|5|13|Raises your power and speed attack by two steps for two turns; deals large damage\n" + \
                         "KH0.2 Terra & Ventus|Upright|Speed|Single|x3.4|5|13|Raises your power and speed attack by two steps for two turns; deals large damage\n" + \
                         "KH0.2 Terra & Ventus|Upright|Speed|Single|x3.4|5|13|Raises your power and speed attack by two steps for two turns; deals large damage"
        obtained_table = prepare_reply_body([self.combat_medal]*20)

        self.assertEqual(obtained_table, expected_table)

