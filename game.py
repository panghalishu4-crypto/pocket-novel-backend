import random

# Step 2: Uska randint function use karo (1 se 6 ke beech)
dice_roll = random.randint(1, 6)

print("Aapka Dice Number Aaya:", dice_roll)
a = random.randint(1, 10)
print("your no.", a)
b = random.choice(["ishu", "parshant", "aman", "anuj"])
print("name", b)
cards = [1, 2, 3, 4, 5]
random.shuffle(cards)
print("Shuffled Cards:", cards)
d = random.shuffle([1, 2, 3, 4, 5])
print("your card", d)

import math
print(math.sqrt(25))
print(math.pow(5, 4))
print(math.ceil(4.7))
print(math.floor(5.9))
print(math.pi)

import datetime
print(datetime.datetime.now())
print(datetime.date.today())
now = datetime.datetime.now()
e = now.strftime("%d-%m-%Y %I:%M %p")
print("this is", e)