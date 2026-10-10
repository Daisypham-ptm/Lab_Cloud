## 1. Hàm `estimate()`

```
estimate(compute_hours, hourly_rate, storage_gb, storage_rate, requests, per_million, egress_gb,egress_rate) 
-> dict[str, str]
```

### Tham số

| Tham số | Ý nghĩa | Đơn vị | Điều kiện |
|---|---|---|---|
| `compute_hours` | Số giờ compute sử dụng | giờ | hữu hạn, ≥ 0 |
| `hourly_rate` | Đơn giá compute | tiền/giờ | hữu hạn, ≥ 0 |
| `storage_gb` | Dung lượng lưu trữ cấp phát (tính cả tháng) | GB | hữu hạn, ≥ 0 |
| `storage_rate` | Đơn giá lưu trữ | tiền/GB-tháng | hữu hạn, ≥ 0 |
| `requests` | Tổng số request | request | hữu hạn, ≥ 0 |
| `per_million` | Đơn giá cho mỗi 1.000.000 request | tiền/triệu request | hữu hạn, ≥ 0 |
| `egress_gb` | Lưu lượng dữ liệu ra ngoài | GB | hữu hạn, ≥ 0 |
| `egress_rate` | Đơn giá egress | tiền/GB | hữu hạn, ≥ 0 |

Đầu vào là số hoặc chuỗi số hợp lệ; giá trị âm, NaN hoặc vô cực gây `ValueError`.

### Công thức

```
compute_cost  = compute_hours × hourly_rate
storage_cost  = storage_gb × storage_rate
requests_cost = (requests / 1.000.000) × per_million
egress_cost   = egress_gb × egress_rate

total_cost    = compute_cost + storage_cost + requests_cost + egress_cost
```
### Ví dụ

Dữ liệu đầu vào (minh họa): 60 hoặc 720 giờ compute, 0.04/giờ; 10 GB lưu trữ, 0.02/GB-tháng; 2.000.000 request, 0.20/triệu; 5 GB egress, 0.09/GB.

| Thành phần | Công thức | Kịch bản 60 giờ | Kịch bản 720 giờ |
|---|---|---|---|
| Compute | `compute_hours × hourly_rate` | 60 × 0.04 = **2.40** | 720 × 0.04 = **28.80** |
| Storage | `storage_gb × storage_rate` | 10 × 0.02 = **0.20** | 10 × 0.02 = **0.20** |
| Requests | `(requests / 1.000.000) × per_million` | (2.000.000 / 1.000.000) × 0.20 = **0.40** | **0.40** |
| Egress | `egress_gb × egress_rate` | 5 × 0.09 = **0.45** | 5 × 0.09 = **0.45** |
| **Tổng** | cộng 4 thành phần | 2.40 + 0.20 + 0.40 + 0.45 = **3.45** | 28.80 + 0.20 + 0.40 + 0.45 = **29.85** |

## Hàm `workers()`

```
workers(rate, per_worker, tolerated_failures=0) -> int
```

### Chú thích tham số

| Tham số | Ý nghĩa | Đơn vị | Điều kiện |
|---|---|---|---|
| `rate` | Nhu cầu tải cần xử lý | request/giây | hữu hạn, ≥ 0 |
| `per_worker` | Năng lực xử lý của mỗi worker | request/giây/worker | hữu hạn, > 0 |
| `tolerated_failures` | Số worker được phép hỏng mà hệ thống vẫn đủ tải | worker | số nguyên, ≥ 0 (mặc định 0) |

### Công thức

```
base_workers = ceil(rate / per_worker)
workers      = base_workers + tolerated_failures
```

### Ví dụ

Dữ liệu đầu vào: `rate` = 180 request/s, `per_worker` = 40 request/s, `tolerated_failures` = 1.

| Bước | Công thức | Tính toán | Kết quả |
|---|---|---|---|
| 1. Nhu cầu / năng lực | `rate / per_worker` | 180 / 40 | 4,5 |
| 2. Làm tròn lên | `ceil(4,5)` | ceil(4,5) | **5** |
| 3. Cộng dự phòng | `base_workers + tolerated_failures` | 5 + 1 | **6** |
