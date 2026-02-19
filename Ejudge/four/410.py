def cycle_list(lst, k):
    for _ in range(k):
        for item in lst:
            yield item


lst = input().split()
k = int(input())

for value in cycle_list(lst, k):
    print(value, end=" ")
