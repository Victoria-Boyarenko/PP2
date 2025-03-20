from functools import reduce
import math
import time

#1
def multiply_list(numbers):
    return reduce(lambda x, y: x * y, numbers)

#2
def count_upper_lower(s):
    upper = sum(1 for char in s if char.isupper())
    lower = sum(1 for char in s if char.islower())
    return upper, lower
 
 #3
def is_palindrome(s):
    return s == s[::-1]

#4
def delayed_sqrt(number, delay_ms):
    time.sleep(delay_ms / 1000)   
    return math.sqrt(number)

#5
def all_true(t):
    return all(t)

print("Multiplication of list: ", multiply_list([1, 2, 3, 4, 5]))
print("Upper and lower count: ", count_upper_lower("Hello World"))
print("Is palindrome: ", is_palindrome("madam"))
print("Square root after delay: ", delayed_sqrt(25100, 2123))
print("All elements true: ", all_true((True, True, False)))




