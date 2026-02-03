def is_valid(n: str) -> bool:
    for digit in n:
        if int(digit) % 2 != 0:
            return False
    return True


n = input().strip()

if is_valid(n):
    print("Valid")
else:
    print("Not valid")
