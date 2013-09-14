from unittest import TestCase
from simulation import greatest_pair_of_factors

__author__ = 'olga_andreyeva'


class TestGreatestPairOfFactors(TestCase):
    def test_greatest_pair_of_factors(self):
        self.assertEqual(greatest_pair_of_factors(5), (5, 1))
        self.assertEqual(greatest_pair_of_factors(20), (5, 4))
        self.assertEqual(greatest_pair_of_factors(16), (4, 4))
