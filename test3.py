for i in range(1, 6):
    print("number: ", i)
    print(i)
for j in range(1, 10, 3):
    print(j)
for k in range(100, 0, -10):
    print(k)
num = int(input("enter the number of tabe you want:"))
for l in range(1, 11):
    print(f"{num} * {l} = {num*l}")

total = 0

for m in range(1, 11):
    total = total + m

print("1 se 10 tak ke numbers ka Total Sum: ", total)

i = 1
while i <= 5:
    i = i + 1
    print(i)
i = 1
while i <= 5:
    
    print(i)
    i = i + 1

for i in range(1, 6):
    if i == 3:
        continue
    print("number", i)

fruits = ["apple", "mango", "banana", "cherry", "grapes", "papaya"]
for fruit in fruits:
    if fruit == "grapes":
        print("we found grapes🍇")
        break
else: 
    print("we didn't found grapes!")

#a game now😁

secret_number = 5
for attempt in range(1, 4):
    guess = int(input("guess a number between 1 to 10: "))
    if guess == secret_number:
        print("congratulations, you guessed correct🥰")
        break
    else:
        print("try again!!, wrong answer❌")

print("game over!!")

items = ["😊", "🥰", "✨", "👌", 1]
items.insert(1, "❤️")
print("--my beautiful store--")
for heart in items:
    print("it's cute", heart)

marks = [11, 22, 33, 44, 55, 66, 77, 88, 99, 00]
print(len(marks))
print(min(marks))
print(max(marks))
print(sum(marks))

total_marks = [80, 88, 77, 99, 89]
pass_students = []
fail_students = []
for mark in total_marks:
    if mark >= 80:
        pass_students.append(mark)
    else:
        fail_students.append(mark)
print("total students: ", len(total_marks))
print("pass students: ", pass_students)
print("fail students: ", fail_students)
print("top marks: ", max(total_marks))

numbers = [1, 2, 2, 3, 4, 4, 4, 5]

print(list(set(numbers)))

###################################################################################
#dictinary
student = {"name": "ishu",
 "age": "22",
 "doing": "learning"
 }
print(student)

get_n = input("enter your name: ").strip().capitalize()
get_a = int(input("enter your age: ").strip())
get_d = input("tell me what are you doing?: ").strip().lower()
students = {"Name": get_n,
            "Age": get_a,
             "Doing": get_d
             }
students["hehe"] = "haha"
print(students)
for k in student.keys():
    print("key: ", k)

stu = {}
for i in range(2):
    roll_no = int(input("enter your roll number: ").strip())
    namee = get_n
    stu[roll_no] = namee
print("student data: ", stu)

for h,j in student.items():
    print(h, "--->", j)
students["hehe"]

all = {"name": "ishu", "age": "22", "city": "sonipat"}
remove = all.pop("city")
print("jo hta hn", remove)
print("jo left hn", all)
