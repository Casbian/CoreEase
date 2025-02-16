#!/usr/bin/env python3
"""
This is a test file for lexer and parser.
It includes various Python language constructs for testing purposes.
"""
import sys
import math
import random
import json
import re
GLOBAL_VAR = 42
def welcome():
    print("Welcome to the test file for lexer and parser!")
    print("This file includes various language constructs.")
def factorial(n):
    if n < 0:
        raise ValueError("Negative values not allowed")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
# A function that tests arithmetic operations
def arithmetic_test():
    a = 10
    b = 3
    print("Addition:", a + b)
    print("Subtraction:", a - b)
    print("Multiplication:", a * b)
    print("Division:", a / b)
    print("Integer Division:", a // b)
    print("Modulus:", a % b)
    print("Exponentiation:", a ** b)
def string_operations():
    s1 = "Hello"
    s2 = 'World'
    s3 = """Multi-line
string using triple quotes"""
    print(s1, s2)
    print(s3)
    print("Concatenation: " + s1 + " " + s2)
    print("Repetition: " + s1 * 3)
class TestClass:
    class_variable = "I am a class variable"
    def __init__(self, value):
        self.value = value
        self.history = [value]
    def update(self, new_value):
        self.value = new_value
        self.history.append(new_value)
    def display(self):
        print("Current value:", self.value)
        print("History:", self.history)
    @staticmethod
    def static_method_example():
        print("This is a static method")
    @classmethod
    def class_method_example(cls):
        print("This is a class method")
        print("Class variable:", cls.class_variable)
square = lambda x: x * x
def list_and_generator():
    numbers = [i for i in range(10)]
    squares = [square(n) for n in numbers]
    gen = (n for n in numbers if n % 2 == 0)
    print("Numbers:", numbers)
    print("Squares:", squares)
    print("Even numbers from generator:", list(gen))
def error_handling():
    try:
        print("Trying to compute factorial of -1")
        print(factorial(-1))
    except ValueError as e:
        print("Caught an error:", e)
    finally:
        print("Completed error handling test")
# A function that tests recursion with a nested function
def recursive_test(n):
    def inner_recursion(x):
        if x <= 0:
            return 0
        return x + inner_recursion(x - 1)
    result = inner_recursion(n)
    print("Sum from 1 to", n, "is", result)
    return result
def dictionary_operations():
    d = {'a': 1, 'b': 2, 'c': 3}
    print("Original dictionary:", d)
    d['d'] = 4
    print("After adding key 'd':", d)
    for key, value in d.items():
        print("Key:", key, "Value:", value)
    squared = {k: v*v for k, v in d.items()}
    print("Squared values:", squared)
def set_operations():
    set1 = set([1, 2, 3, 4])
    set2 = set([3, 4, 5, 6])
    print("Set1:", set1)
    print("Set2:", set2)
    print("Union:", set1.union(set2))
    print("Intersection:", set1.intersection(set2))
    print("Difference (set1 - set2):", set1.difference(set2))
def file_operations():
    filename = "temp_test_file.txt"
    try:
        with open(filename, "w") as f:
            f.write("This is a test file.\n")
            f.write("It is used for testing file operations.\n")
        with open(filename, "r") as f:
            content = f.read()
            print("File content:")
            print(content)
    except IOError as e:
        print("File error:", e)
    finally:
        import os
        if os.path.exists(filename):
            os.remove(filename)
# A main function to run all tests
def main():
    print("----- Welcome Message -----")
    welcome()
    print("\n----- Arithmetic Test -----")
    arithmetic_test()
    print("\n----- String Operations -----")
    string_operations()
    print("\n----- Factorial Test -----")
    for i in range(6):
        print("Factorial of", i, "is", factorial(i))
    print("\n----- Fibonacci Test -----")
    for i in range(10):
        print("Fibonacci of", i, "is", fibonacci(i))
    print("\n----- List and Generator Test -----")
    list_and_generator()
    print("\n----- Error Handling Test -----")
    error_handling()
    print("\n----- Recursive Test -----")
    recursive_test(5)
    print("\n----- Dictionary Operations -----")
    dictionary_operations()
    print("\n----- Set Operations -----")
    set_operations()
    print("\n----- File Operations -----")
    file_operations()
    print("\n----- Class and Methods Test -----")
    obj = TestClass(10)
    obj.display()
    obj.update(20)
    obj.display()
    TestClass.static_method_example()
    TestClass.class_method_example()
    print("\n----- Lambda Function Test -----")
    print("Square of 7 is", square(7))
    print("\n----- End of Tests -----")
if __name__ == "__main__":
    main()