n = int(input())
arr = list(map(int, input().split()))
q = int(input())

operations = []

for _ in range(q):
    parts = input().split()
    op = parts[0]

    if op == "add":
        x = int(parts[1])
        operations.append(lambda a, x=x: a + x)

    elif op == "multiply":
        x = int(parts[1])
        operations.append(lambda a, x=x: a * x)

    elif op == "power":
        x = int(parts[1])
        operations.append(lambda a, x=x: a ** x)

    elif op == "abs":
        operations.append(lambda a: abs(a))

for func in operations:
    arr = list(map(func, arr))

print(*arr)
