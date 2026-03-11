n = int(input())
numbers = list(map(int, input().split()))
a = list(filter(lambda x: (x % 2 == 0), numbers))

print(len(a))