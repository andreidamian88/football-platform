
import unittest
import sys
from pathlib import Path

# Locate the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Allow Python to find our analysis script
sys.path.insert(0, str(PROJECT_ROOT / "06_Scripts"))

# Import the functions we want to test
from club_behaviour_fingerprint import (
     calculate_lead_protection,
     calculate_comeback_win_rate,
     classify_evidence
)


class TestClubBehaviourFingerprint(unittest.TestCase):

    def test_lead_protection(self):
        result = calculate_lead_protection(4, 3)
        self.assertEqual(result, 75.00)

    def test_lead_protection_with_zero_opportunities(self):
        result = calculate_lead_protection(0, 0)
        self.assertIsNone(result)

    def test_comeback_win_rate(self):
        result = calculate_comeback_win_rate(4, 2)
        self.assertEqual(result, 50.00)

    def test_comeback_win_rate_with_zero_opportunities(self):
        result = calculate_comeback_win_rate(0, 0)
        self.assertIsNone(result)

    def test_lead_protection_rounding(self):
        result = calculate_lead_protection(3, 2)
        self.assertEqual(result, 66.67)

    def test_lead_protection_with_zero_successes(self):
        result = calculate_lead_protection(10, 0)
        self.assertEqual(result, 0.0)

    def test_evidence_no_opportunities(self):
        self.assertEqual(classify_evidence(0), "No evidence")

    def test_evidence_very_limited(self):
        self.assertEqual(classify_evidence(1), "Very limited")
        self.assertEqual(classify_evidence(3), "Very limited")

    def test_evidence_limited(self):
        self.assertEqual(classify_evidence(5), "Limited")

    def test_evidence_developing(self):
        self.assertEqual(classify_evidence(10), "Developing")

    def test_evidence_stronger(self):
        self.assertEqual(classify_evidence(20), "Stronger")