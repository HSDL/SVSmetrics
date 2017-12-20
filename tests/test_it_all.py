import unittest
import pkg_resources
import SVSmetrics


class Test(unittest.TestCase):

    def test_null(self):
        print("\n")
        temp = SVSmetrics.Corpus(pkg_resources.resource_filename('tests', 'test.csv'))
        temp.compute_individual_variety()
        # print(temp.participant_data.to_string)
        temp._generate_nominal_team(2, {'Level': '==1'})
        self.assertEqual(True, True)
