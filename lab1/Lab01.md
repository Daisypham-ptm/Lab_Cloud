# HW01: Cloud foundations and economics

**Lecture:** deck 01, emphasis on slides 03–23. **Suggested effort:** 1.5–2 hours.

Size and price an examination service using an explicit illustrative model.

## Interface

`estimate(compute_hours, hourly_rate, storage_gb, storage_rate, requests, per_million, egress_gb, egress_rate) -> dictionary of decimal strings; workers(rate, per_worker, tolerated_failures=0) -> integer.`

Implement `lab01.py`. Run your own tests with `python3 -m unittest discover -s . -p 'test*.py' -v` from your submission folder.

## Requirements

1. Implement compute, storage, request, and egress cost components using Decimal arithmetic. Return compute, storage, requests, egress, and total as strings with two decimal places. Sum unrounded components before formatting; use Decimal default ROUND_HALF_EVEN.
2. Reject negative and nonfinite cost inputs with ValueError. Inputs are numeric values or valid numeric strings; no currency symbols are supplied.
3. Implement ceiling-based worker sizing, then add the requested failure headroom. Capacity inputs are finite nonnegative demand, positive per-worker capacity, and an integer nonnegative failure count.
4. Calculate the supplied case: 60 compute hours at 0.04/hour, 10 GB at 0.02/GB-month, 2,000,000 requests at 0.20/million, and 5 GB egress at 0.09/GB. Treat storage as a full-month allocation.
5. Compare it with 720 compute hours while other inputs stay unchanged. Size 180 requests/s at 40 requests/s per worker with tolerance for one worker loss.
6. Write an assumption table and label every rate as illustrative. List three excluded charges. Do not present these rates as current AWS/Azure/GCP quotations.

## Acceptance checklist

- [ ] The component sum equals the total before rounding.
- [ ] Zero usage has zero usage charges; a negative input fails.
- [ ] Worker count uses ceiling, not rounding to nearest.
- [ ] Your report separates estimated costs from measured bills.

## Progressive hints

1. Convert through Decimal(str(value)) to avoid importing binary floating-point error.
2. Requests are billed in units of one million in this exercise, not individually.
3. Compute the workers needed after a failure, then add the failed worker.

## Discussion questions

1. Why does Little’s law not establish p95 latency?
2. When is a 60-hour estimate an unfair comparison with an always-on service?
3. Does using two providers automatically improve availability?

