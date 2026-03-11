n = int(input())
nums = list(map(int, input().split()))

count_truthy = sum(map(bool, nums))
print(count_truthy)