lines = []
while True:
    line = input()
    if line == "":
        break
    lines.append(line)
paragraph = "n/".join(lines)


age = input("enter your age: ").strip()
if age == "":
    age = "bad boy!"
else:
    age = "no words!"
print("your age is", age)

agge = int(input("enter your age: "))
has_license = input("do you have license (true or false): ").strip().lower()
if agge >= 20 and has_license == "true":
    print("you can drive.")
else:
    print("you can't drive.")

day = input("what is the day today?: ").strip().lower()
if day == "saturday" or day == "sunday":
    print("enjoy, today is holiday ☺")
else:
    print("you have to work, it's working day!")

agee = int(input("enter your age: "))
status = "Adult" if agee >= 18 else "Minor"
print(status)
if agee >= 18:
    print("you can enter")

    has_id = input("do you have id proof? (yes or no): ").strip().lower()
    if has_id == "yes":
        print("you can give the test ☺")
    else:
        print("you can't give the test!")
elif agee == 20:
     print("you can try good options ☻")
else:
    print("you are under 18, so you can't enter!")

for i in range(1, 6):
    print("number: ", i)

#########################################################################################

try:
    a = int(input("enter your number (default no.:0): ").strip())
    b = int(input("enter your number (default no.:0): ").strip())
    ans = a/b

    print("your no. is", ans)
    
except ValueError:
    print("try again, enter only digit!")

except ZeroDivisionError:
    print("try again, enter only digit!")


#######################################################################################
days = ("mon", "tue", "wed", "thu", "fri")
print(days)
print(type(days))
print(days[1])

num = (10, 20, 10, 10, 10, 10)
result = num.count(10)
print(result)
pos = num.index(20)
print(pos)

numb = {10, 20, 20, 30, 10}
print(numb)
numb.add(100)
numb.add(80)
numb.discard(70)
print(numb)