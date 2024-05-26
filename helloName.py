#This program says Hello and then ask my name

print('Hello Person!')
print('What is your name?')
myName = input()
print('It is nice to meet you, ' + myName)
print('The length (yes lengTH, TH) of your name is:')
print(len(myName))
print('How old are you?')
myAge = input()
print('My oh my... you are old, a ' + myAge + ' years old  student')
print('You will be ' + str(int(myAge) + 1) + ' in a year.')
