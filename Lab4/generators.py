def squares(N):
    for i in range(N):
        yield i ** 2

N=int(input("N= "))
for num in squares(N):
    print(num, end=" ")


def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

n = int(input("\nEnter a number: "))
print(", ".join(map(str, even_numbers(n))))


def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n = int(input("\nEnter a number: "))
print("Numbers divisible by 3 and 4:", list(divisible_by_3_and_4(n)))


def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

a, b = map(int, input("\nEnter a and b separated by a space: ").split())
for num in squares(a, b):
    print(num, end=" ")


def countdown(n):
    for i in range(n, -1, -1):
        yield i

n = int(input("\nEnter a number: "))
for num in countdown(n):
    print(num, end=" ")

