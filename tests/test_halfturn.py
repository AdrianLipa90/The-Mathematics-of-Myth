import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mythmath.halfturn import analyze_half_turn


class HalfTurnTests(unittest.TestCase):
    def test_enoch_72_exact_half_turn(self):
        data = json.loads((ROOT / "data" / "1_enoch_ch72_solar_cycle.json").read_text())
        result = analyze_half_turn(data["east_portal"], data["day_parts"])

        self.assertTrue(result.exact)
        self.assertEqual(result.length, 12)
        self.assertEqual(result.half_period, 6)
        self.assertEqual(result.x_pair_sum, Fraction(7, 1))
        self.assertEqual(result.y_pair_sum, Fraction(18, 1))
        self.assertEqual(result.center_x, Fraction(7, 2))
        self.assertEqual(result.center_y, Fraction(9, 1))

    def test_perturbation_breaks_exactness(self):
        x = [4, 5, 6, 6, 5, 4, 3, 2, 1, 1, 2, 3]
        y = [10, 11, 12, 11, 10, 9, 8, 7, 6, 7, 8, 10]
        self.assertFalse(analyze_half_turn(x, y).exact)

    def test_odd_cycle_rejected(self):
        with self.assertRaises(ValueError):
            analyze_half_turn([1, 2, 3], [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
