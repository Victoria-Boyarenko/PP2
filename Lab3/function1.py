def grams_ounces(grams):
    return grams * 28.3495231

def F_to_C(F):
    return (5 / 9) * (F - 32)

def solve(numheads, numlegs):
    for chickens in range (numheads+1):
        rabbits = numheads - chickens
        if 2 * chickens + 4 * rabbits == numlegs:
            return chickens, rabbits
    return "There is no solution"

def is_prime(n):
    if n <= 1:
        return False   
    for i in range(2, n):  
        if n % i == 0:  
            return False   
    return True   

def filter_prime(numbers):
    numbers = numbers.split()  
    numbers_list = []   
    for num in numbers:
        number = int(num)   
        numbers_list.append(number)   

    prime_numbers = [] 
    for num in numbers_list:
        if is_prime(num):   
            prime_numbers.append(num)   

    return prime_numbers  

def get_permutations(s, step=0):
    if step == len(s):
        print("".join(s))
    for i in range(step, len(s)):
        s_copy = list(s)
        s_copy[step], s_copy[i] = s_copy[i], s_copy[step]
        get_permutations(s_copy, step + 1)

def reverse_sentence(sentence):
    words = sentence.split()   
    words.reverse()   
    reversed_sentence = " ".join(words)  
    return reversed_sentence   

def has_33(nums):
    for i in range(len(nums) - 1):
        if nums[i] == 3 and nums[i + 1] == 3:
            return True
    return False

def spy_game(nums):
    sequence = [0, 0, 7]
    index = 0
    
    for num in nums:
        if num == sequence[index]:
            index += 1
            if index == len(sequence):
                return True
    return False

import math

def sphere_volume(radius):
    volume = (4/3) * math.pi * (radius ** 3)
    return volume

def unique_list(list):
    unique = []
    for i in list:
        if i not in unique:
            unique.append(i)
    return unique

def is_palindrome(word):
    word = word.lower()
    cleaned_word = ""
    for char in word:
        if char.isalnum():   
            cleaned_word += char

    return cleaned_word == cleaned_word[::-1]

def histogram(numbers):
    for num in numbers:
        print("*" * num)

import random

def guess_number_game():
    name = input("Hello! What is your name? ")
    print(f"Well, {name}, I am thinking of a number between 1 and 20.")
    secret_number = random.randint(1, 20)
    guesses = 0
    while True:
        g = int(input("Take a guess: "))
        guesses += 1
        if g < secret_number:
            print("Your guess is too low.")
        elif g > secret_number:
            print("Your guess is too high.")
        else:
            print(f"Good job, {name}! You guessed my number in {guesses} guesses!")
            break



print("100 grams to ounces:", grams_ounces(100))
print("34F to Celsius:", F_to_C(34))
print("Filter primes from '10 15 17 19 20':", filter_prime("10 15 17 19 20"))
print("Volume of sphere with radius 5:", sphere_volume(5))
print("Has consecutive 3s in [1, 3, 3, 5]:", has_33([1, 3, 3, 5]))