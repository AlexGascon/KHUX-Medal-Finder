import unittest

from src.comment_parser import CommentParser


class TestCommentParser(unittest.TestCase):

    # ELEMENT CHECK
    def test_element_power_medals(self):
        comment = "Blablablablabla power blablablabla"

        parser = CommentParser(comment)
        parser.extract_requirements()

        self.assertCountEqual(parser.requirements['elements'], ['Power'])


    def test_element_speed(self):
        comment = "Blablablablabla speed blablablabla"

        parser = CommentParser(comment)
        parser.extract_requirements()

        self.assertCountEqual(parser.requirements['elements'], ['Speed'])


    def test_element_magic(self):
        comment = "Blablablablabla magic blablablabla"

        parser = CommentParser(comment)
        parser.extract_requirements()

        self.assertCountEqual(parser.requirements['elements'], ['Magic'])


    def test_element_several_elements(self):
        comment = "Blablablablabla power speed blablablabla"

        parser = CommentParser(comment)
        parser.extract_requirements()

        self.assertCountEqual(parser.requirements['elements'], ['Power', 'Speed'])


    def test_element_psm(self):
        comment = "Blablablablabla PSM blablablabla"

        parser = CommentParser(comment)
        parser.extract_requirements()

        self.assertCountEqual(parser.requirements['elements'], ['Speed', 'Power', 'Magic'])


    def test_element_is_case_insensitive(self):
        comment1 = "Blablablablabla POWER blablablabla"
        comment2 = "Blablab SPEED lablabla MAGIC blablablabla"
        comment3 = "Blablablablabla PSM blablablabla"

        parser1 = CommentParser(comment1)
        parser2 = CommentParser(comment2)
        parser3 = CommentParser(comment3)
        parser1.extract_requirements()
        parser2.extract_requirements()
        parser3.extract_requirements()

        self.assertCountEqual(parser1.requirements['elements'], ['Power'])
        self.assertCountEqual(parser2.requirements['elements'], ['Magic', 'Speed'])
        self.assertCountEqual(parser3.requirements['elements'], ['Power', 'Magic', 'Speed'])
        
        
    # TARGETS CHECK
    def test_targets_single(self):
        comment = "blablablabla single blablabla"
        
        parser = CommentParser(comment)
        parser.extract_requirements()

        self.assertCountEqual(parser.requirements['targets'], ['Single'])
        
    
    def test_targets_aoe(self):
        comment = "blablablabla aoe blablabla"

        parser = CommentParser(comment)
        parser.extract_requirements()

        self.assertCountEqual(parser.requirements['targets'], ['All'])


    def test_targets_random(self):
        comment = "blablablabla random blablabla"

        parser = CommentParser(comment)
        parser.extract_requirements()

        self.assertCountEqual(parser.requirements['targets'], ['Random'])


    def test_targets_multi(self):
        comment = "blablablabla multi blablabla"

        parser = CommentParser(comment)
        parser.extract_requirements()

        self.assertCountEqual(parser.requirements['targets'], ['All'])


    def test_targets_several(self):
        comment = "blablablabla single aoe random blablabla"

        parser = CommentParser(comment)
        parser.extract_requirements()

        self.assertCountEqual(parser.requirements['targets'], ['Single', 'All', 'Random'])


    def test_targets_all_doesnt_triger_anything(self):
        comment = "blablablabla all blablabla"

        parser = CommentParser(comment)
        parser.extract_requirements()

        self.assertCountEqual(parser.requirements['targets'], [])


    def test_targets_is_case_insensitive(self):
        comment = "blablablabla SINGLE AOE blablabla"

        parser = CommentParser(comment)
        parser.extract_requirements()

        self.assertCountEqual(parser.requirements['targets'], ['Single', 'All'])


    # DIRECTION CHECK
    def test_direction_upright(self):
        comment = "blabla upright blabla"

        parser = CommentParser(comment)
        parser.extract_requirements()

        self.assertCountEqual(parser.requirements['direction'], ['Upright'])

    def test_direction_reversed(self):
        comment = "blabla reversed blabla"

        parser = CommentParser(comment)
        parser.extract_requirements()

        self.assertCountEqual(parser.requirements['direction'], ['Reversed'])

    def test_direction_both_directions(self):
        comment = "blabla upright reversed blabla"

        parser = CommentParser(comment)
        parser.extract_requirements()

        self.assertCountEqual(parser.requirements['direction'], ['Upright', 'Reversed'])

    def test_direction_is_case_insensitive(self):
        comment = "blabla UPRIGHT REVERSED blabla"

        parser = CommentParser(comment)
        parser.extract_requirements()

        self.assertCountEqual(parser.requirements['direction'], ['Upright', 'Reversed'])

