import unittest
import pkg_resources
import SVSmetrics


class Test(unittest.TestCase):

    def test_null(self):
        print("\n")
        SVSmetrics.Corpus(pkg_resources.resource_filename('tests', 'test.csv'))
        self.assertEqual(True, True)
