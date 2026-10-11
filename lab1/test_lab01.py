import unittest
from decimal import Decimal
from lab01 import estimate, workers

BASE = dict(storage_gb=10, storage_rate="0.02", requests=2_000_000,
            per_million="0.20", egress_gb=5, egress_rate="0.09",
            hourly_rate="0.04")


def est(compute_hours=60, **over):
    args = dict(BASE, compute_hours=compute_hours)
    args.update(over)
    return estimate(**args)


class TestEstimate(unittest.TestCase):
    def test_case_60_hours(self):
        self.assertEqual(est(60), {"compute": "2.40", "storage": "0.20",
                                   "requests": "0.40", "egress": "0.45",
                                   "total": "3.45"})

    def test_case_720_hours(self):
        r = est(720)
        self.assertEqual(r["compute"], "28.80")
        self.assertEqual(r["total"], "29.85")

    def test_only_compute_changes(self):
        a, b = est(60), est(720)
        for k in ("storage", "requests", "egress"):
            self.assertEqual(a[k], b[k])

    def test_all_values_are_strings_two_decimals(self):
        for v in est(60).values():
            self.assertIsInstance(v, str)
            self.assertEqual(len(v.split(".")[1]), 2)

    def test_keys(self):
        self.assertEqual(set(est(60)),
                         {"compute", "storage", "requests", "egress", "total"})

    def test_zero_usage(self):
        r = estimate(0, "0.04", 0, "0.02", 0, "0.20", 0, "0.09")
        # storage is a full-month allocation: 0 GB -> 0 charge
        self.assertTrue(all(v == "0.00" for v in r.values()))

    def test_total_summed_before_rounding(self):
        # each component = 0.004 -> rounds to 0.00, but total = 0.016 -> 0.02
        r = estimate("0.1", "0.04", "0.2", "0.02", 20000, "0.20", "0.04", "0.1")
        self.assertEqual(r["compute"], "0.00")
        self.assertEqual(r["storage"], "0.00")
        self.assertEqual(r["requests"], "0.00")
        self.assertEqual(r["egress"], "0.00")
        self.assertEqual(r["total"], "0.02")

    def test_half_even_rounding(self):
        # 0.125 -> 0.12 ; 0.135 -> 0.14 (round half to even)
        self.assertEqual(estimate("0.125", 1, 0, 0, 0, 0, 0, 0)["compute"], "0.12")
        self.assertEqual(estimate("0.135", 1, 0, 0, 0, 0, 0, 0)["compute"], "0.14")

    def test_no_float_error(self):
        # 0.1 * 3 must be exactly 0.30
        self.assertEqual(estimate(3, 0.1, 0, 0, 0, 0, 0, 0)["compute"], "0.30")

    def test_string_and_numeric_inputs(self):
        self.assertEqual(est("60", hourly_rate=Decimal("0.04"))["total"], "3.45")

    def test_requests_billed_per_million(self):
        self.assertEqual(estimate(0, 0, 0, 0, 500_000, "0.20", 0, 0)["requests"], "0.10")

    def test_negative_rejected_each_argument(self):
        good = [60, "0.04", 10, "0.02", 2_000_000, "0.20", 5, "0.09"]
        for i in range(len(good)):
            bad = list(good)
            bad[i] = -1
            with self.subTest(arg=i):
                with self.assertRaises(ValueError):
                    estimate(*bad)

    def test_nonfinite_rejected(self):
        for bad in (float("nan"), float("inf"), float("-inf"), "NaN", "Infinity"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    est(bad)

    def test_invalid_string_rejected(self):
        for bad in ("abc", "$5", "", None):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    est(bad)

    def test_negative_zero_not_printed(self):
        self.assertEqual(estimate("-0", 1, 0, 0, 0, 0, 0, 0)["compute"], "0.00")


class TestWorkers(unittest.TestCase):
    def test_supplied_case(self):
        self.assertEqual(workers(180, 40, 1), 6)

    def test_ceiling_not_round(self):
        self.assertEqual(workers(180, 40), 5)     
        self.assertEqual(workers(161, 40), 5)      
        self.assertEqual(workers(1, 1000), 1)

    def test_exact_division(self):
        self.assertEqual(workers(160, 40), 4)
        self.assertEqual(workers(160, 40, 2), 6)

    def test_zero_demand(self):
        self.assertEqual(workers(0, 40), 0)
        self.assertEqual(workers(0, 40, 1), 1)

    def test_default_failures_zero(self):
        self.assertEqual(workers(100, 25), 4)

    def test_decimal_and_string_inputs(self):
        self.assertEqual(workers("0.3", "0.1"), 3)  
        self.assertEqual(workers(Decimal("180"), "40", 1), 6)

    def test_invalid_rate(self):
        for bad in (-1, float("nan"), float("inf"), "abc"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    workers(bad, 40)

    def test_invalid_per_worker(self):
        for bad in (0, -5, float("nan"), float("inf"), "abc"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    workers(180, bad)

    def test_invalid_failures(self):
        for bad in (-1, 1.5, 1.0, "1", None, True):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    workers(180, 40, bad)


if __name__ == "__main__":
    unittest.main()