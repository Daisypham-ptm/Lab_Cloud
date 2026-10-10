# Complete every function.
"""Illustrative cost model; these inputs are NOT provider prices."""
import math
from decimal import Decimal, ROUND_HALF_EVEN, InvalidOperation

def estimate(compute_hours, hourly_rate, storage_gb, storage_rate, requests, per_million, egress_gb, egress_rate):
    inputs = [compute_hours, hourly_rate, storage_gb, storage_rate, requests, per_million, egress_gb, egress_rate]
    decimals = []
    for val in inputs:
        try:
            d = Decimal(str(val))
        except (InvalidOperation, TypeError, ValueError):
            raise ValueError(f"Giá trị đầu vào không hợp lệ: {val}")
        if d.is_nan() or d.is_infinite() or d < Decimal('0'):
            raise ValueError(f"Giá trị đầu vào phải là số hữu hạn không âm, nhận được: {val}")
        decimals.append(d)
        
    c_hours, c_rate, s_gb, s_rate, req, req_rate, e_gb, e_rate = decimals

    compute_cost = c_hours * c_rate
    storage_cost = s_gb * s_rate
    requests_cost = (req / Decimal('1000000')) * req_rate
    egress_cost = e_gb * e_rate

    total_cost = compute_cost + storage_cost + requests_cost + egress_cost

    def format_two_decimals(val):
        return str(val.quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN))

    return {
        "compute": format_two_decimals(compute_cost),
        "storage": format_two_decimals(storage_cost),
        "requests": format_two_decimals(requests_cost),
        "egress": format_two_decimals(egress_cost),
        "total": format_two_decimals(total_cost)
    }

def workers(rate, per_worker, tolerated_failures=0):
    # Chuyển đầu vào sang decimal
    try:
        demand = Decimal(str(rate))
        capacity = Decimal(str(per_worker))
    except Exception:
        raise ValueError("Đầu vào phải là giá trị số")

    # Nhu cầu phải không âm, năng lực mỗi worker phải dương
    if demand < 0:
        raise ValueError("rate phải không âm")

    if capacity <= 0:
        raise ValueError("per_worker phải là dương")

    # Số worker lỗi cho phép phải là số nguyên không âm
    if tolerated_failures < 0 or type(tolerated_failures) != int:
        raise ValueError("tolerated_failures phải là số nguyên không âm")

    # Tính số worker cơ sở bằng phép làm tròn lên
    base_workers = int(
        (demand / capacity).to_integral_value(rounding=ROUND_CEILING)
    )

    # Cộng thêm worker dự phòng để chịu được số worker bị lỗi
    return base_workers + tolerated_failures
