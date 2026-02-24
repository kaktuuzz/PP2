#Create a generator that generates the squares of numbers up to some number N
def square(N):
    for i in range(N + 1):
        yield i * i
N = int(input())
for i in square(N):
    print(i)

#Write a program using generator to print the even numbers between 0 and n in comma separated form where n is input from console
def evennumbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i
n = int(input())
for i in evennumbers(n):
    print(i, end=",")

#Define a function with a generator which can iterate the numbers, which are divisible by 3 and 4, between a given range 0 and n
def divisible(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
for i in divisible(20):
    print(i, end=' ')

#Implement a generator called squares to yield the square of all numbers from (a) to (b). Test it with a "for" loop and print each of the yielded values.
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i
for i in squares(3, 7):
    print(i)

#Implement a generator that returns all numbers from (n) down to 0.
def countdown(n):
    for i in range(n, -1, -1):
        yield i
for i in countdown(5):
    print(i, end=' ')