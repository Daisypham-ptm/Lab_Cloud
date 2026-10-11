import math
from decimal import Decimal, ROUND_HALF_EVEN, InvalidOperation, ROUND_CEILING

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
        q = val.quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)
        # SỬA Ở ĐÂY: Dùng q.is_zero() để bắt đúng cả Decimal('-0.00') lẫn Decimal('0.00')
        if q.is_zero():
            return "0.00"
        return str(q)

    return {
        "compute": format_two_decimals(compute_cost),
        "storage": format_two_decimals(storage_cost),
        "requests": format_two_decimals(requests_cost),
        "egress": format_two_decimals(egress_cost),
        "total": format_two_decimals(total_cost)
    }
