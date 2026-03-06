import re

# Match a string that has 'a' followed by zero or more 'b'

pattern = r"ab*"
text = "abbb a ab aaaa"

matches = re.findall(pattern, text)
print(matches)


# Match a string that has 'a' followed by two to three 'b'

pattern = r"ab{2,3}"
text = "ab abb abbb abbbb"

matches = re.findall(pattern, text)
print(matches)


# Find sequences of lowercase letters joined with an underscore

pattern = r"[a-z]+_[a-z]+"
text = "hello_world test_example wrong_Example another_one"

matches = re.findall(pattern, text)
print(matches)

# Find sequences of one uppercase letter followed by lowercase letters

pattern = r"[A-Z][a-z]+"
text = "Hello world Python Is Great"

matches = re.findall(pattern, text)
print(matches)


# Match a string that has 'a' followed by anything, ending in 'b'

pattern = r"a.*b"
text = "acb a123b axxxb ab a_test_b"

matches = re.findall(pattern, text)
print(matches)


# Replace all occurrences of space, comma, or dot with a colon

text = "Hello, world. Python is fun"
result = re.sub(r"[ ,\.]", ":", text)

print(result)


# Convert snake_case string to camelCase

def snake_to_camel(text):
    return re.sub(r"_([a-z])", lambda x: x.group(1).upper(), text)

text = "hello_world_python"
print(snake_to_camel(text))


# Split a string at uppercase letters

text = "HelloWorldPythonIsCool"
result = re.split(r"(?=[A-Z])", text)

print(result)


# Insert spaces between words starting with capital letters

text = "HelloWorldPython"
result = re.sub(r"([A-Z])", r" \1", text).strip()

print(result)



# Convert camelCase string to snake_case

def camel_to_snake(text):
    return re.sub(r"([A-Z])", r"_\1", text).lower()

text = "helloWorldPython"
print(camel_to_snake(text))