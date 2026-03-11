n = int(input())
a = list(map(int, input().split()))
sum = 0
for i in a:
   b = i * i
   sum = sum + b
print(sum)