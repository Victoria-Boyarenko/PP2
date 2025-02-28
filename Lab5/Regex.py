import re

#1
pattern = "ab*"
string = "ac ab abb abbb"

matches = re.findall(pattern, string)
print(matches)   

#2
pattern = "ab{2,3}"
string = "ab a abbb abb abс"

matches = re.findall(pattern, string)
print(matches)   

#3
pattern = "[a-z]+_[a-z]+"
string = "abc_def gh_ij klm_nop AVV_GGH advf"

matches = re.findall(pattern, string)
print(matches) 

#4
pattern = "[A-Z][a-z]+"
string = "Apple banana Peach coconut Orange"

matches = re.findall(pattern, string)
print(matches)  

#5
pattern = "a.*b"
string = "acb a123b axb abb ab acd afggh45"

matches = re.findall(pattern, string)
print(matches)   

#6
pattern = "[ ,.]"
string = "Hello, how are you?"

new_string = re.sub(pattern, ":", string)
print(new_string)  

#7
def snake_to_camel(snake_str):
    words = snake_str.split('_')
    capitalized_words = [word.capitalize() for word in words]
    camel_case_str = ''.join(capitalized_words)
    return camel_case_str

string = "hello_world_python"
result = snake_to_camel(string)

print("CamelCase:", result)

#8
pattern = "([A-Z])"
string = "SplitByUppercaseLetters"

split_string = re.sub(pattern, " \\1", string).strip()
print(split_string) 

#9
pattern = "([A-Z])"
string = "InsertspacesBetweenWords"

new_string = re.sub(pattern, " \\1", string).strip()
print(new_string)  

#10
def camel_to_snake(camel_str):
    snake_str = ''
    for char in camel_str:
        if char.isupper():
            if snake_str:   
                snake_str += '_'
            snake_str += char.lower()
        else:
            snake_str += char
    
    return snake_str

string = "HelloWorldPython"
result = camel_to_snake(string)

print("snake_case:", result)
