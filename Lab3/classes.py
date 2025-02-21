class StringManipulator:
    def __init__(self):
        self.text = ""  

    def getString(self):
        self.text = input("Enter the line: ")   

    def printString(self):
        print(self.text.upper())  

 
obj = StringManipulator()
obj.getString()   
obj.printString()   


class Shape:
    def area(self):
        return 0   

class Square(Shape):
    def __init__(self, length):
        self.length = length  

    def area(self):
        return self.length ** 2   

square = Square(6)
print(square.area())   


class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

rectangle = Rectangle(2, 5)
print(rectangle.area())  



import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        print(f"Point: ({self.x}, {self.y})")

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def dist(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

 
p1 = Point(1, 2)
p2 = Point(3, 4)

p1.show()   
p1.move(5, 6)
p1.show()   

print(p1.dist(p2))  



class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Replenishment: {amount}. Current balance: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Error: Insufficient funds")
        else:
            self.balance -= amount
            print(f"Withdrawal: {amount}. Remains: {self.balance}")

 
acc = Account("Aiulum", 1000)
acc.deposit(600)   
acc.withdraw(300)   
acc.withdraw(1500)  


def is_prime(n):
    if n <= 1:
        return False   
    for i in range(2, n):  
        if n % i == 0:  
            return False   
    return True  
numbers = [10, 3, 5, 8, 11, 14, 17, 19, 21, 23, 29, 30]
prime_numbers = list(filter(lambda x: is_prime(x), numbers))

print("Prime numbers:", prime_numbers)
