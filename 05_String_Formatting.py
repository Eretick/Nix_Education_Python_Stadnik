'''task from https://www.learnpython.org/en/String_Formatting'''
data = ("John", "Doe", 53.44)

# correct variant from task page
format_string = "Hello %s %s. Your current balance is $%s."
# my variant with the same result. Didn't passed the test. Why?
format_string2 = "Hello %s %s. Your current balance is $%.2f."
print(format_string % data)
#print(format_string2 % data)