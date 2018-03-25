import unittest

from khux_medal_finder.comment import RequirementExtractor


class TestCommentParser(unittest.TestCase):

    # ELEMENT CHECK
    def test_element_power_medals(self):
        comment = "Blablablablabla power blablablabla"

        extractor = RequirementExtractor(comment)
        extractor.extract_requirements()

        self.assertCountEqual(extractor.requirements['elements'], ['Power'])


    def test_element_speed(self):
        comment = "Blablablablabla speed blablablabla"

        extractor = RequirementExtractor(comment)
        extractor.extract_requirements()

        self.assertCountEqual(extractor.requirements['elements'], ['Speed'])


    def test_element_magic(self):
        comment = "Blablablablabla magic blablablabla"

        extractor = RequirementExtractor(comment)
        extractor.extract_requirements()

        self.assertCountEqual(extractor.requirements['elements'], ['Magic'])


    def test_element_several_elements(self):
        comment = "Blablablablabla power speed blablablabla"

        extractor = RequirementExtractor(comment)
        extractor.extract_requirements()

        self.assertCountEqual(extractor.requirements['elements'], ['Power', 'Speed'])


    def test_element_psm(self):
        comment = "Blablablablabla PSM blablablabla"

        extractor = RequirementExtractor(comment)
        extractor.extract_requirements()

        self.assertCountEqual(extractor.requirements['elements'], ['Speed', 'Power', 'Magic'])


    def test_element_is_case_insensitive(self):
        comment1 = "Blablablablabla POWER blablablabla"
        comment2 = "Blablab SPEED lablabla MAGIC blablablabla"
        comment3 = "Blablablablabla PSM blablablabla"

        extractor1 = RequirementExtractor(comment1)
        extractor2 = RequirementExtractor(comment2)
        extractor3 = RequirementExtractor(comment3)
        extractor1.extract_requirements()
        extractor2.extract_requirements()
        extractor3.extract_requirements()

        self.assertCountEqual(extractor1.requirements['elements'], ['Power'])
        self.assertCountEqual(extractor2.requirements['elements'], ['Magic', 'Speed'])
        self.assertCountEqual(extractor3.requirements['elements'], ['Power', 'Magic', 'Speed'])
        
        
    # TARGETS CHECK
    def test_targets_single(self):
        comment = "blablablabla single blablabla"
        
        extractor = RequirementExtractor(comment)
        extractor.extract_requirements()

        self.assertCountEqual(extractor.requirements['targets'], ['Single'])
        
    
    def test_targets_aoe(self):
        comment = "blablablabla aoe blablabla"

        extractor = RequirementExtractor(comment)
        extractor.extract_requirements()

        self.assertCountEqual(extractor.requirements['targets'], ['All'])


    def test_targets_random(self):
        comment = "blablablabla random blablabla"

        extractor = RequirementExtractor(comment)
        extractor.extract_requirements()

        self.assertCountEqual(extractor.requirements['targets'], ['Random'])


    def test_targets_multi(self):
        comment = "blablablabla multi blablabla"

        extractor = RequirementExtractor(comment)
        extractor.extract_requirements()

        self.assertCountEqual(extractor.requirements['targets'], ['All'])


    def test_targets_several(self):
        comment = "blablablabla single aoe random blablabla"

        extractor = RequirementExtractor(comment)
        extractor.extract_requirements()

        self.assertCountEqual(extractor.requirements['targets'], ['Single', 'All', 'Random'])


    def test_targets_all_doesnt_triger_anything(self):
        comment = "blablablabla all blablabla"

        extractor = RequirementExtractor(comment)
        extractor.extract_requirements()

        self.assertCountEqual(extractor.requirements['targets'], [])


    def test_targets_is_case_insensitive(self):
        comment = "blablablabla SINGLE AOE blablabla"

        extractor = RequirementExtractor(comment)
        extractor.extract_requirements()

        self.assertCountEqual(extractor.requirements['targets'], ['Single', 'All'])


    # DIRECTION CHECK
    def test_direction_upright(self):
        comment = "blabla upright blabla"

        extractor = RequirementExtractor(comment)
        extractor.extract_requirements()

        self.assertCountEqual(extractor.requirements['direction'], ['Upright'])

    def test_direction_reversed(self):
        comment = "blabla reversed blabla"

        extractor = RequirementExtractor(comment)
        extractor.extract_requirements()

        self.assertCountEqual(extractor.requirements['direction'], ['Reversed'])

    def test_direction_both_directions(self):
        comment = "blabla upright reversed blabla"

        extractor = RequirementExtractor(comment)
        extractor.extract_requirements()

        self.assertCountEqual(extractor.requirements['direction'], ['Upright', 'Reversed'])

    def test_direction_is_case_insensitive(self):
        comment = "blabla UPRIGHT REVERSED blabla"

        extractor = RequirementExtractor(comment)
        extractor.extract_requirements()

        self.assertCountEqual(extractor.requirements['direction'], ['Upright', 'Reversed'])

