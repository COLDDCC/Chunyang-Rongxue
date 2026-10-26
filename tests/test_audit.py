import unittest
from scripts.audit import validate, DIMENSIONS, GATES

def base():
    return {
        "product": "test", "mode": "build",
        "weights": dict(zip(DIMENSIONS, (15, 20, 20, 15, 10, 10, 10))),
        "scores": {k: {"score": 80, "evidence": "Observed test"} for k in DIMENSIONS},
        "gates": {k: "pass" for k in GATES},
    }

class AuditTests(unittest.TestCase):
    def test_fully_valid(self):
        errors, result = validate(base())
        self.assertFalse(errors)
        self.assertEqual(result["weighted_score"], 80)
        self.assertTrue(result["acceptance_eligible"])

    def test_missing_evidence(self):
        d = base()
        d["scores"]["ux"]["evidence"] = ""
        self.assertTrue(validate(d)[0])

    def test_unknown_gate_blocks(self):
        d = base()
        d["gates"]["core_task"] = "unknown"
        self.assertFalse(validate(d)[1]["acceptance_eligible"])

    def test_partial_does_not_claim_full(self):
        d = base()
        del d["scores"]["seo"]
        result = validate(d)[1]
        self.assertEqual(result["coverage"], "partial")
        self.assertFalse(result["acceptance_eligible"])

    def test_invalid_weight(self):
        d = base()
        d["weights"]["seo"] = 20
        self.assertTrue(validate(d)[0])

if __name__ == "__main__":
    unittest.main()
