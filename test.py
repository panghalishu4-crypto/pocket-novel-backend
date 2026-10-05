print("Hello World!")
print("i am learning.")
print("my name is ishu")
print("i am", 21,"years old")
print("i am", 11 + 11, "years old")
print("i am", 11 +11, "years old")
print("i am", 11+11, "years old")
5+5 == 10
age = 11 + 11
name = "ishu"
print("i am", name, "i am", age, "years old")
print(5+5)
print(age)


name = "anshu"
height = 5.1
nature = True 
print("i am", name, "and my height is", height)
print(name)
print(age)
print(height)
print(type(name))
print(type(height))
print(type(age))
print(type(nature))
naam = input("enter your name: ")
teri_age = int(input("may i know your birth year? "))
print("welcome,", naam)
print("so you are", teri_age, "years old")
so_age = int(input("may i know your age? "))
print("so you would be", so_age+2, "next year.")
if so_age >= 18:
    print("you can do it!")
else:
    print("you can't do it! you are minor.")

marks = float(input("enter your marks: "))
if marks >= 80:
    print("you got A grade.")
elif marks >= 50:
    print("you did well, you pass the exam.")
else:
    print("you need to improvement, you failed.")

right_now_age = 2026 - teri_age
print("hello,", naam, "so you are", right_now_age, "years old this year.")

first = int(input("first person birth year: "))
second = int(input("second person birth year: "))
third = int(input("third person birth year: "))
first_age = 2026 - first
second_age = 2026 - second
third_age = 2026 - third

print("you are", first_age, "years old.")
print("you are", second_age, "years old.")
print("you are", third_age, "years old.")
if first_age > 20:
    print("it's good.")
elif second_age > 20:
    print("it's good.")
elif third_age > 20:
    print("it's good.")
else:
    print("they are all we got.")

a = 3+2
b = "trip"
print(b+str(a))

a_name, b_age, c_city = input("Enter your name, age, city (enter space between them): ").split()
a_name, b_age, c_city = input("Enter your name, age, city (enter comma between them): ").split(",")

import getpass
password = getpass.getpass("enter your password: ")

markss = list(map(int, input("Enter your marks: ").split()))
print(markss)
print(type(markss[1]))
marksss = list(map(int, input("enter your marks: ").split()))
try:
    agee = list(map(int, input("enter your age: ").split()))
    print("your age is", agee)
except ValueError:
    print("the letter or word you entered is not valid, please enter number or digit!")

cityy = list(input("enter you city (DEfault: Delhi): ").split())
if cityy == "":
    cityy = "Delhi"

print("your city is ", cityy)

cityyy = input("enter your city: ") or "Delhi"
print(cityyy)
ans = input("enter yes or no: ").strip().upper()
print("your answer is ", ans)

lines = []
while True:
    line = input()
    if line == "":
        break
    lines.append(line)
paragraph = "n/".join(lines)


agge = input("enter your age: ").split().strip()
if agge == "":
    agge = "bad boy!"
elif agge >= 18:
    agge = "okay, good boy!"
else:
    agge = "no words!"
print("your age is ", agge)