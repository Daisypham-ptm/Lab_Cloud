# HW01: Cloud Foundations and Economics

**Course:** Cloud Computing
**Group:** 3
**Supervisor:** Hàn Trung Định
**University:** Trường Đại học Giao thông Vận tải TP. Hồ Chí Minh, Viện Công nghệ Thông tin và Điện, Điện tử
**Date:** Ho Chi Minh City, October 15, 2026

**Submitted files:** `lab01.py` (code) and `Report_Lab01_Group_3.md` (this report, including the test code and test results).

## Contents

1. Team Task Assignment
2. Assignment Requirements
3. Assumption Table
4. Itemized Cost Comparison
5. Worker Sizing
6. Excluded Charges and Estimate vs Measured Bill
7. Test Results
8. Discussion Questions
9. Submission Checklist
10. References
11. Appendix: test_lab01.py

---

## 1. Team Task Assignment

| Full name | Student ID | Assigned tasks | Progress |
| --- | --- | --- | --- |
| Nguyễn Minh Khôi | 089206024791 | Worker calculation and result analysis | 100% |
| Phạm Thị Muội | 052306002706 | Writing tests and program testing | 100% |
| Nguyễn Thị Thanh Nhàn | 048306000418 | Discussion questions and final compilation | 100% |
| Võ Dương Huỳnh Như | 094306000511 | Cost and assumptions report | 100% |
| Phan Tấn Lộc | 087207007721 | Cost calculation code | 100% |

## 2. Assignment Requirements

**Lecture:** deck 01, emphasis on slides 03–23. **Suggested effort:** 1.5–2 hours.

Size and price an examination service using an explicit illustrative model.

**Interface**

```
estimate(compute_hours, hourly_rate, storage_gb, storage_rate, requests, per_million, egress_gb, egress_rate) -> dictionary of decimal strings
workers(rate, per_worker, tolerated_failures=0) -> integer
```

Implement `lab01.py`. Run your own tests with `python3 -m unittest discover -s . -p 'test*.py' -v` from your submission folder.

**Requirements**

1. Implement compute, storage, request, and egress cost components using Decimal arithmetic. Return compute, storage, requests, egress, and total as strings with two decimal places. Sum unrounded components before formatting; use Decimal default ROUND_HALF_EVEN.
2. Reject negative and nonfinite cost inputs with ValueError. Inputs are numeric values or valid numeric strings; no currency symbols are supplied.
3. Implement ceiling-based worker sizing, then add the requested failure headroom. Capacity inputs are finite nonnegative demand, positive per-worker capacity, and an integer nonnegative failure count.
4. Calculate the supplied case: 60 compute hours at 0.04/hour, 10 GB at 0.02/GB-month, 2,000,000 requests at 0.20/million, and 5 GB egress at 0.09/GB. Treat storage as a full-month allocation.
5. Compare it with 720 compute hours while other inputs stay unchanged. Size 180 requests/s at 40 requests/s per worker with tolerance for one worker loss.
6. Write an assumption table and label every rate as illustrative. List three excluded charges. Do not present these rates as current AWS/Azure/GCP quotations.

**Acceptance checklist**

- The component sum equals the total before rounding.
- Zero usage has zero usage charges; a negative input fails.
- Worker count uses ceiling, not rounding to nearest.
- Your report separates estimated costs from measured bills.

**Progressive hints**

1. Convert through `Decimal(str(value))` to avoid importing binary floating-point error.
2. Requests are billed in units of one million in this exercise, not individually.
3. Compute the workers needed after a failure, then add the failed worker.

**Discussion questions**

1. Why does Little's law not establish p95 latency?
2. When is a 60-hour estimate an unfair comparison with an always-on service?
3. Does using two providers automatically improve availability?

## 3. Assumption Table

The cost model is established based on assumed operational parameters and dated as of October 12, 2026. All rates are illustrative and are not current AWS, Azure, or GCP quotations.

| Cost Item | Assumed Usage Level | Illustrative Unit Price (USD) | Basis and Calculation Rules |
| --- | --- | --- | --- |
| Virtual Machine Compute | 60 hours & 720 hours | 0.0400 / hour | Calculated based on total virtual machine active uptime. |
| Provisioned Storage | 10 GB | 0.0200 / GB-month | Fixed block storage allocation provisioned for the entire month. |
| Request Volume | 2,000,000 requests | 0.2000 / 1,000,000 requests | Billed per unit of one million processed requests. |
| Outbound Data Egress | 5 GB | 0.0900 / GB | Volume of data transferred out of the cloud infrastructure. |

## 4. Itemized Cost Comparison

The figures are computed with Python's Decimal arithmetic (not binary floating point) to prevent precision errors. All unrounded component costs are summed first, then each value is formatted to two decimal places using ROUND_HALF_EVEN.

| Cost Item | Calculation Formula | 60-Hour Scenario (USD) | 720-Hour Scenario (USD) | Cost Share (720h) |
| --- | --- | --- | --- | --- |
| Virtual Machine Compute | Compute Hours × Hourly Rate | 2.40 | 28.80 | 96.48% |
| Provisioned Storage | Storage Volume (GB) × Monthly Rate | 0.20 | 0.20 | 0.67% |
| Request Volume | (Request Count / 1,000,000) × Rate per Million | 0.40 | 0.40 | 1.34% |
| Outbound Data Egress | Egress Volume (GB) × Rate per GB | 0.45 | 0.45 | 1.51% |
| **TOTAL ESTIMATED COST** | **Sum of 4 unrounded components** | **3.45** | **29.85** | **100.00%** |

Inputs are numbers or valid numeric strings; negative, NaN or infinite values raise ValueError. Zero usage gives a charge of 0.00.

**Analysis of cost variation when increasing compute duration (60 hours to 720 hours)**

- **Linear compute scaling vs. sub-linear total growth:** virtual machine compute cost increases exactly 12-fold (from $2.40 to $28.80). However, the total cost grows only about 8.65 times (from $3.45 to $29.85). This occurs because non-compute resources (storage $0.20 + requests $0.40 + egress $0.45 = $1.05) represent a fixed cost baseline regardless of compute hours.
- **Shift in cost distribution:** in the 60-hour scenario, compute represents 69.57% of total expenditure. When scaling to 720 hours (continuous 24/7 monthly operation), compute becomes the overwhelming financial driver, accounting for 96.48% of the monthly bill while fixed component shares diminish.
- **Fairness of comparison and availability realities:** comparing a 60-hour run directly against a 720-hour deployment represents two fundamentally different service availability levels. A 60-hour estimate models short-term or on-demand usage, whereas a 720-hour deployment represents an always-on service with continuous readiness, persistent background dependencies, and different SLA commitments.

## 5. Worker Sizing

Demand 180 requests/s; capacity 40 requests/s per worker; tolerate the loss of one worker.

| Step | Formula | Calculation | Result |
| --- | --- | --- | --- |
| 1. Demand / capacity | rate / per_worker | 180 / 40 | 4.5 |
| 2. Round up | ceil(4.5) | ceil(4.5) | 5 |
| 3. Add headroom | base_workers + tolerated_failures | 5 + 1 | **6** |

Check: after losing one worker, 5 × 40 = 200 ≥ 180 requests/s. Conditions: rate is finite and ≥ 0, per_worker is finite and > 0, tolerated_failures is an integer ≥ 0.

## 6. Excluded Charges and Estimate vs Measured Bill

**Three excluded charges not included in the simplified model**

In actual commercial cloud invoices, three major categories of charges are excluded from this basic estimation model but incur real costs:

1. **Orphaned storage volumes, snapshots, and log storage:** residual unattached storage volumes remaining active after instance termination, storage fees for volume backup snapshots, and ingestion/retention charges for system audit logs.
2. **Networking gateways and unattached secondary resources:** hourly charges for NAT gateways and application load balancers, and holding fees for unattached static public IP addresses.
3. **Taxes, currency exchange, and paid technical support plans:** applicable value-added taxes (VAT), foreign currency conversion fees, and optional paid enterprise technical support tiers from cloud providers.

**Distinguishing estimated costs from measured bills**

- **Estimated cost:** a theoretical projection based on fixed unit prices and pre-defined usage metrics, assuming an idealized operating state without workload volatility or unexpected infrastructure overhead.
- **Measured (actual) bill:** the official billed amount based on real consumption data. Invoices are subject to actual traffic spikes, burstable data egress, provider minimum billing granularity rules, applicable taxes, and currency exchange rate fluctuations.

**Financial risk control**

- **Budget alerts:** automated notifications triggered when expenditure approaches defined thresholds. Budget alerts function purely as notifications and do not automatically terminate running resources.
- **Resource quotas and access policies:** hard limits on maximum instance counts, storage capacity, and egress bandwidth to proactively prevent unbudgeted cost overruns.

## 7. Test Results

Test command (run from the submission folder):

```
python3 -m unittest discover -s . -p 'test*.py' -v
```

The test file `test_lab01.py` contains 24 automated tests (full code in the Appendix). The first run found 3 failing cases; after the fixes, all 24 tests pass.

**Table 1: Defects found and fixed**

| # | Defect | Input causing it | Detecting test | Cause | Fix |
| --- | --- | --- | --- | --- | --- |
| 1 | `workers()` raised TypeError instead of ValueError | `tolerated_failures = "1"` | `test_invalid_failures` | The comparison `< 0` ran before the type check | Check the type first: `type(tolerated_failures) is not int or tolerated_failures < 0` |
| 2 | `workers()` raised TypeError instead of ValueError | `tolerated_failures = None` | `test_invalid_failures` | Same as defect 1 | Same as defect 1 |
| 3 | `estimate()` printed `"-0.00"` instead of `"0.00"` | `compute_hours = "-0"` | `test_negative_zero_not_printed` | `Decimal('-0')` keeps its negative sign after rounding | In `format_two_decimals`, return `"0.00"` when `q.is_zero()` |

**Table 2: Test results before and after the fixes**

| Run | Tests | Passed | Failed | Conclusion |
| --- | --- | --- | --- | --- |
| Before the fixes | 24 | 21 | 3 (1 failure, 2 errors) | FAILED |
| After the fixes | 24 | 24 | 0 | OK |

**Table 3: Test coverage**

| Group | What is checked | Related requirement |
| --- | --- | --- |
| Main results | 60 hours → total 3.45; 720 hours → total 29.85; only compute changes | Requirements 4, 5 |
| Format | Results are two-decimal strings; all 5 keys present | Requirement 1 |
| Rounding | Sum before rounding, half-even, no floating-point error | Requirement 1, hint 1 |
| Requests | Billed in units of one million | Hint 2 |
| Zero usage | Zero input gives "0.00" everywhere | Acceptance checklist |
| Invalid input | Negative, NaN, infinite, invalid strings | Requirement 2 |
| Workers | Ceiling (not rounding to nearest), exact division, zero demand, failure headroom | Requirements 3, 5 |
| Wrong-type failures | Negative, 1.5, 1.0, "1", None, True | Requirement 3 |

**Output of the first run (before the fixes):**

```
FAIL: test_negative_zero_not_printed
AssertionError: '-0.00' != '0.00'
ERROR: test_invalid_failures (bad='1')
TypeError: '<' not supported between instances of 'str' and 'int'
ERROR: test_invalid_failures (bad=None)
TypeError: '<' not supported between instances of 'NoneType' and 'int'

Ran 24 tests
FAILED (failures=1, errors=2)
```

**Output after the fixes:**

```
test_all_values_are_strings_two_decimals (test_lab01.TestEstimate.test_all_values_are_strings_two_decimals) ... ok
test_case_60_hours (test_lab01.TestEstimate.test_case_60_hours) ... ok
test_case_720_hours (test_lab01.TestEstimate.test_case_720_hours) ... ok
test_half_even_rounding (test_lab01.TestEstimate.test_half_even_rounding) ... ok
test_invalid_string_rejected (test_lab01.TestEstimate.test_invalid_string_rejected) ... ok
test_keys (test_lab01.TestEstimate.test_keys) ... ok
test_negative_rejected_each_argument (test_lab01.TestEstimate.test_negative_rejected_each_argument) ... ok
test_negative_zero_not_printed (test_lab01.TestEstimate.test_negative_zero_not_printed) ... ok
test_no_float_error (test_lab01.TestEstimate.test_no_float_error) ... ok
test_nonfinite_rejected (test_lab01.TestEstimate.test_nonfinite_rejected) ... ok
test_only_compute_changes (test_lab01.TestEstimate.test_only_compute_changes) ... ok
test_requests_billed_per_million (test_lab01.TestEstimate.test_requests_billed_per_million) ... ok
test_string_and_numeric_inputs (test_lab01.TestEstimate.test_string_and_numeric_inputs) ... ok
test_total_summed_before_rounding (test_lab01.TestEstimate.test_total_summed_before_rounding) ... ok
test_zero_usage (test_lab01.TestEstimate.test_zero_usage) ... ok
test_ceiling_not_round (test_lab01.TestWorkers.test_ceiling_not_round) ... ok
test_decimal_and_string_inputs (test_lab01.TestWorkers.test_decimal_and_string_inputs) ... ok
test_default_failures_zero (test_lab01.TestWorkers.test_default_failures_zero) ... ok
test_exact_division (test_lab01.TestWorkers.test_exact_division) ... ok
test_invalid_failures (test_lab01.TestWorkers.test_invalid_failures) ... ok
test_invalid_per_worker (test_lab01.TestWorkers.test_invalid_per_worker) ... ok
test_invalid_rate (test_lab01.TestWorkers.test_invalid_rate) ... ok
test_supplied_case (test_lab01.TestWorkers.test_supplied_case) ... ok
test_zero_demand (test_lab01.TestWorkers.test_zero_demand) ... ok

----------------------------------------------------------------------
Ran 24 tests in 0.002s

OK
```

**Conclusion:** all 24 tests pass on the final `lab01.py`. The first run exposed three edge-case defects (two type-handling errors in `workers()` and one negative-zero formatting error in `estimate()`), which were fixed and re-tested.

## 8. Discussion Questions

**Q1. Why does Little's law not establish p95 latency?**

Little's law (L = λ × W) shows the relationship between the average number of requests in a system, the arrival rate, and the average time a request spends in the system. For example, if the arrival rate is 120 requests/s and the average response time is 0.25 s, there are about 30 requests in the system on average. However, this does not tell us the p95 latency, because p95 depends on the response times of individual requests, especially the slower ones. Two systems can have the same average response time but different p95 values. Therefore, we need to measure response times under the expected workload to find the p95.

**Q2. When is a 60-hour estimate an unfair comparison with an always-on service?**

A 60-hour estimate is not a fair comparison if the service needs to run all the time. An always-on service may use about 720 compute hours in a 30-day month, while the 60-hour estimate assumes that the service only runs when needed. The two options may also have different start-up delays and availability. In addition, some costs, such as storage or backup, may still be charged even when the compute service is stopped. To compare them fairly, we should use the same workload, time period, availability requirement, and cost categories.

**Q3. Does using two providers automatically improve availability?**

No. Using two cloud providers does not automatically make a service more available. In an idealized model with independent replicas, availability is A = 1 − (1 − a)ⁿ, but this holds only if the failures are independent. The service could still fail if both providers depend on the same data source, network service, identity system, or faulty software release. We also need to set up data replication and a way to switch traffic to the other provider when one fails. These steps should be tested before relying on them. Multi-cloud can improve availability, but only if the system is designed to handle failures across providers.

## 9. Submission Checklist

| Item | Status |
| --- | --- |
| `lab01.py` with `estimate()` and `workers()` completed | 100% |
| `test_lab01.py` (code in the Appendix) | 100% |
| Successful test run output | 100% |
| Cost table for 60 hours and 720 hours | 100% |
| Result of 6 workers with one worker failure headroom | 100% |
| Assumption table and three excluded charges | 100% |
| Answers to the three discussion questions | 100% |
| Consistent figures (3.45 / 29.85 / 6) and one currency convention | 100% |

## 10. References

1. Comer, D. E. (2021). *The cloud computing book: Platform, infrastructure, interfaces, and security* (Chapters 1–4). CRC Press.
2. Marinescu, D. C. (2018). *Cloud computing: Theory and practice* (2nd ed., Chapters 1–2). Morgan Kaufmann.

## 11. Appendix: test_lab01.py

```python
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
        self.assertEqual(workers(180, 40), 5)      # 4.5 -> 5
        self.assertEqual(workers(161, 40), 5)      # 4.025 -> 5 (round() would give 4)
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
        self.assertEqual(workers("0.3", "0.1"), 3)  # float would give 4
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
```
