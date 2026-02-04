#Lambda functions are commonly used with built-in functions like map(), filter(), and sorted().


numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)