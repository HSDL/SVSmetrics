import unittest
import pkg_resources
import SVSmetrics


class Test(unittest.TestCase):

    def test_null(self) -> None:
        # Read in the data
        temp = SVSmetrics.Corpus(pkg_resources.resource_filename('tests', 'designs.csv'),
                                 pkg_resources.resource_filename('tests', 'participants.csv'))

        # Make sure we're only dealing with one level
        temp.remove_participants("Level", 1)

        # Compute variety for individuals
        temp.compute_individual_variety()

        # Get all conditions
        v, c = temp.get_all_conditions(100, 4)

        self.assertEqual(True, True)
