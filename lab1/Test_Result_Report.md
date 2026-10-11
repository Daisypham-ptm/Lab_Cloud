# Báo cáo kiểm thử HW01

## Bảng 1: Danh sách lỗi đã xử lý

| # | Lỗi | Đầu vào gây lỗi | Test phát hiện | Nguyên nhân | Cách sửa |
|---|---|---|---|---|---|
| 1 | `workers()` ném `TypeError` thay vì `ValueError` | `tolerated_failures = "1"` | `test_invalid_failures` | Phép `< 0` chạy trước khi kiểm tra kiểu | Kiểm tra kiểu trước: `type(tolerated_failures) is not int or tolerated_failures < 0` |
| 2 | `workers()` ném `TypeError` thay vì `ValueError` | `tolerated_failures = None` | `test_invalid_failures` | Như lỗi 1 | Như lỗi 1 |
| 3 | `estimate()` in `"-0.00"` thay vì `"0.00"` | `compute_hours = "-0"` | `test_negative_zero_not_printed` | `Decimal('-0')` sau khi làm tròn vẫn mang dấu âm | Trong `format_two_decimals`, nếu `q.is_zero()` thì trả về `"0.00"` |

## Bảng 2: Kết quả chạy test trước và sau khi sửa

| Lần chạy | File kết quả | Số test | Qua | Không qua | Kết luận |
|---|---|---|---|---|---|
| Trước khi sửa | `test_results_before.txt` | 24 | 21 | 3 (1 failure, 2 errors) | `FAILED` |
| Sau khi sửa | `test_results_after.txt` | 24 | 24 | 0 | `OK` |

## Bảng 3: Phạm vi kiểm thử

| Nhóm | Nội dung kiểm tra | Yêu cầu đề liên quan |
|---|---|---|
| Kết quả chính | 60 giờ → total 3.45; 720 giờ → total 29.85; chỉ compute thay đổi | Yêu cầu 4, 5 |
| Định dạng | Kết quả là chuỗi 2 chữ số thập phân, đủ 5 khóa | Yêu cầu 1 |
| Làm tròn | Cộng trước khi làm tròn, half-even, không lỗi float | Yêu cầu 1, hint 1 |
| Request | Tính theo đơn vị 1 triệu | Hint 2 |
| Zero usage | Đầu vào 0 cho ra toàn `"0.00"` | Checklist |
| Đầu vào sai | Âm, NaN, vô cực, chuỗi không hợp lệ | Yêu cầu 2 |
| Workers | Ceiling (không làm tròn thường), chia hết, demand = 0, dự phòng lỗi | Yêu cầu 3, 5 |
| Failures sai kiểu | Âm, 1.5, 1.0, `"1"`, `None`, `True` | Yêu cầu 3 |

## Kết luận

Nhóm đã viết 24 test tự động. Lần chạy đầu phát hiện 3 lỗi ở các trường hợp biên (2 lỗi kiểu dữ liệu trong `workers()`, 1 lỗi dấu `-0` trong `estimate()`). Sau khi sửa, cả 24 test đều qua.
