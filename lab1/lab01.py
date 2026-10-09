# Complete every function.
"""Illustrative cost model; these inputs are NOT provider prices."""
from decimal import Decimal, ROUND_CEILING
import json

def estimate(compute_hours, hourly_rate, storage_gb, storage_rate, requests, per_million, egress_gb, egress_rate):
    raise NotImplementedError('Implement according to the assignment')

def workers(rate, per_worker, tolerated_failures=0):
    raise NotImplementedError('Implement according to the assignment')
