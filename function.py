def num():
    print("lets see what it can do?")
num()

fruits = input("enter the fruit you want to eat: ").strip().lower()
def see(fruits):
    print(fruits, "ka shake bn rha hn")
see(fruits)

def make_shake(fruit):
    print(fruit, " ka shake ban kar tayar hai!")
make_shake("mango")

see("avakado")

def add(a, b):
    sum = a + b
    return sum
    result = add(list(map(int, input("enter the numbers to sum: ").split())))
print()


##############################################################

def ishu():
    print("i am ishu❤️")
ishu()

name = input("enter you name: ").strip().lower()
def greet():
    print("hey👋", name)
greet()

def greeting(name):
    print("Good Morning", name)
greeting(name)

def hehe(a, b):
    haha = a + b
    return haha
c = int(input("enter 1st no.: ").strip())
d = int(input("enter 2nd no.: ").strip())
ishuu = hehe(c, d)
print(ishuu)

def country(country_name = "usa"):
    print("this is your country name: ", country_name)
e = input("enter your country name: ").strip().lower()
if e == "":
    country()
else:
    country(e)


def things(thing_name = "box"):
    print("these are your things: ", thing_name)
get_thing = input("enter your thing names: ").strip().lower()
if get_thing == "":
    things()
else:
    things(get_thing)

######################################################################################
def chije(*item):
    for i in item:
        print(i.strip())
get = input("enter your thing you wanna order: ").lower()
gets = get.split(",")
chije(*gets)