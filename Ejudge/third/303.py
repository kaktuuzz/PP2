digit = {
    "ZER": "0","ONE": "1","TWO": "2","THR": "3","FOU": "4","FIV": "5", "SIX": "6", "SEV": "7", "EIG": "8", "NIN": "9"
}

reversed = {}
for key in digit:
    value = digit[key]
    reversed[value] = key


def decode(sn):
    number_as_string = ""
    index = 0
    while index < len(sn):
        t = sn[index:index + 3]
        number_as_string += digit[t]
        index += 3
    return int(number_as_string)


def encode(number):
    result = ""
    for digit in str(number):
        result += reversed[digit]
    return result


ex = input().strip()

if "+" in ex:
    parts = ex.split("+")
    o = "+"
elif "-" in ex:
    parts = ex.split("-")
    o = "-"
else:
    parts = ex.split("*")
    o = "*"

left_part = parts[0]
right_part = parts[1]

left_number = decode(left_part)
right_number = decode(right_part)

if o == "+":
    answer = left_number + right_number
elif o == "-":
    answer = left_number - right_number
else:
    answer = left_number * right_number

print(encode(answer))