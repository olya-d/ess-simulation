from unittest import TestCase
from simulation import greatest_pair_of_factors

__author__ = 'olga_andreyeva'


class TestGreatestPairOfFactors(TestCase):
    def test_greatest_pair_of_factors(self):
        self.assertEqual(greatest_pair_of_factors(5), (1, 5))
        self.assertEqual(greatest_pair_of_factors(20), (4, 5))
        self.assertEqual(greatest_pair_of_factors(16), (4, 4))
