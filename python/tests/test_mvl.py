import unittest
from python.helpers.loom_logic import (
    compute_entropy,
    calculate_meaningfulness,
    decide_mt_gate,
    calculate_narrative_weight
)

class TestMVLLogic(unittest.TestCase):
    def test_compute_entropy(self):
        # Initial entropy
        e = 0.5
        # Low novelty increases entropy
        e1 = compute_entropy(e, 0.2, False)
        self.assertAlmostEqual(e1, 0.58)

        # High novelty decreases entropy
        e2 = compute_entropy(e, 0.7, False)
        self.assertAlmostEqual(e2, 0.44)

        # Pattern repeat increases entropy
        e3 = compute_entropy(e, 0.5, True)
        self.assertAlmostEqual(e3, 0.6)

        # Clamping
        self.assertEqual(compute_entropy(0.95, 0.1, True), 1.0)
        self.assertEqual(compute_entropy(0.05, 0.8, False), 0.0)

    def test_calculate_meaningfulness(self):
        # meaningfulness = 0.5*narrative_weight + 0.3*novelty + 0.2*(1-entropy)
        m = calculate_meaningfulness(0.8, 0.6, 0.4)
        # 0.5*0.8 + 0.3*0.6 + 0.2*0.6 = 0.4 + 0.18 + 0.12 = 0.7
        self.assertAlmostEqual(m, 0.7)

    def test_decide_mt_gate(self):
        # silence if meaningfulness < 0.25
        self.assertEqual(decide_mt_gate(0.2, 0.5, False, False, False), "silence")

        # refuse if utility_flag and narrative_weight < 0.5
        self.assertEqual(decide_mt_gate(0.6, 0.4, True, False, False), "refuse")

        # delay if mask_conflict
        self.assertEqual(decide_mt_gate(0.6, 0.6, False, True, False), "delay")

        # confront if meaningfulness > 0.75 and self_sabotage
        self.assertEqual(decide_mt_gate(0.8, 0.8, False, False, True), "confront")

        # reply otherwise
        self.assertEqual(decide_mt_gate(0.6, 0.6, False, False, False), "reply")

    def test_calculate_narrative_weight(self):
        # base weight 0.2
        self.assertAlmostEqual(calculate_narrative_weight(), 0.2)

        # Adding factors
        self.assertAlmostEqual(calculate_narrative_weight(has_desire_fear_confession=True), 0.4)
        self.assertAlmostEqual(calculate_narrative_weight(has_desire_fear_confession=True, references_past=True), 0.6)
        self.assertAlmostEqual(calculate_narrative_weight(has_desire_fear_confession=True, references_past=True, is_decision_point=True, is_identity_statement=True), 1.0)

if __name__ == "__main__":
    unittest.main()
