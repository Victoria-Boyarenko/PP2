from datetime import datetime, timedelta

current_date = datetime.now().date()
date_minus_five = current_date - timedelta(days=5)
print("Current Date:", current_date)
print("Date Minus Five Days:", date_minus_five)


yesterday = current_date - timedelta(days=1)
tomorrow = current_date + timedelta(days=1)
print("\nYesterday:", yesterday)
print("Today:", current_date)
print("Tomorrow:", tomorrow)


current_datetime = datetime.now()
datetime_without_microseconds = current_datetime.replace(microsecond=0)
print("\nCurrent Datetime with Microseconds:", current_datetime)
print("Datetime without Microseconds:", datetime_without_microseconds)


date1 = datetime(2025, 2, 10, 12, 0, 0)
date2 = datetime(2025, 2, 20, 14, 30, 0)
difference_in_seconds = int((date2 - date1).total_seconds())
print("\nDifference in Seconds:", difference_in_seconds)