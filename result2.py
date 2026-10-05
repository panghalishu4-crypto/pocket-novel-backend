


# 1. Input liya aur Comma se tod kar List banayi
items = input("Samaan (comma se): ").split(",")
prices = input("Rates (comma se): ").split(",")

total = 0

# 2. Loop se ek-ek karke bill banaya
for i in range(len(items)):
    rate = int(prices[i])   # Text ko Number banaya
    total = total + rate     # Total me joda
    print(items[i], ": Rs.", rate)

print("Total Bill =", total)


# -------------------------------------------------------------
# STEP 1: User se Comma (,) lagakar saare Items aur Prices maangna
# -------------------------------------------------------------
items_input = input("Samaan ke naam comma (,) lagakar dalo (jaise: Milk, Bread, Egg): ")
price_input = input("Unke rate/price bhi comma (,) lagakar dalo (jaise: 50, 40, 60): ")

# -------------------------------------------------------------
# STEP 2: .split(",") ka use karke alag-alag karke List banana
# -------------------------------------------------------------
items_list = items_input.split(",")
price_string_list = price_input.split(",")

# -------------------------------------------------------------
# STEP 3: Khaali (Empty) variables aur Lists banana
# -------------------------------------------------------------
final_prices = []   # Numbers (Integer) store karne ke liye
total_bill = 0      # Total add karne ke liye

# Price list ke har item par Loop chala kar use Integer me badalna
for price in price_string_list:
    clean_price = int(price.strip()) # strip() extra spaces hatata hai
    final_prices.append(clean_price)

# -------------------------------------------------------------
# STEP 4: Loop chala kar saaman aur price ko ek-ek karke print karna
# -------------------------------------------------------------
print("\n========== AAPKA FINAL BILL ==========")

# range(len(...)) se hum index (0, 1, 2) ke sath loop chalate hain
for i in range(len(items_list)):
    item_name = items_list[i].strip() # Samaan ka naam
    item_price = final_prices[i]      # Samaan ka price
    
    print(f"{i+1}. {item_name} : Rs.{item_price}")
    
    # Total me jodna
    total_bill = total_bill + item_price

print("--------------------------------------")
print("TOTAL BILL AMOUNT : Rs.", total_bill)
print("======================================")



#######################################################################################
# ---------------------------------------------------------
# Step 1: Global Dictionary (Student Data Store Karne Ke Liye)
# ---------------------------------------------------------
students_db = {}


# ---------------------------------------------------------
# Step 2: Functions Banayein (Har Kaam Ki Machine)
# ---------------------------------------------------------

# Function 1: Naya Student Add Karna
def add_student():
    print("\n--- Naya Student Add Karein ---")
    roll_no = int(input("Roll Number dalo: "))

    # Check karna ki Roll No pehle se toh nahi hai
    if roll_no in students_db:
        print("❌ Yeh Roll Number pehle se majood hai!")
        return

    name = input("Student ka naam dalo: ").strip().lower()
    age = int(input("Student ki age dalo: "))
    course = input("Course ka naam dalo: ").strip().lower()

    # Dictionary ke andar inner dictionary save karna
    students_db[roll_no] = {"Name": name, "Age": age, "Course": course}
    print("✅ Student safaltapoorvak add ho gaya!")


# Function 2: Saare Students Ka Data Dikhana
def view_all_students():
    print("\n--- Saare Students Ka Data ---")
    if not students_db:
        print("⚠️ Abhi koi student add nahi hua hai.")
        return

    # Loop chala kar dictionary se data nikalna
    for roll, info in students_db.items():
        print(
            f"Roll No: {roll} | Name: {info['Name'].capitalize()} | Age: {info['Age']} | Course: {info['Course'].upper()}"
        )


# Function 3: Roll Number Se Dhoondhna (.get() Safe Method)
def search_student():
    print("\n--- Student Dhoondhein ---")
    roll_no = int(input("Dhoondhne ke liye Roll Number dalo: "))

    student = students_db.get(roll_no)

    if student:
        print(f"✅ Student Mila!")
        print(f"Name  : {student['Name'].capitalize()}")
        print(f"Age   : {student['Age']}")
        print(f"Course: {student['Course'].upper()}")
    else:
        print("❌ Yeh Roll Number nahi mila!")


# ---------------------------------------------------------
# Step 3: Main Program Loop (While Loop Menu)
# ---------------------------------------------------------
while True:
    print("\n==============================")
    print("  STUDENT MANAGEMENT SYSTEM")
    print("==============================")
    print("1. Naya Student Add Karein")
    print("2. Saare Students Dekhein")
    print("3. Roll Number Se Search Karein")
    print("4. Exit (Program Band Karein)")

    choice = input("Apna option chunein (1-4): ").strip()

    if choice == "1":
        add_student()
    elif choice == "2":
        view_all_students()
    elif choice == "3":
        search_student()
    elif choice == "4":
        print("\nDhanyawad! Program band ho raha hai. 👋")
        break
    else:
        print("❌ Galat option! Kripya 1, 2, 3 ya 4 hi chunein.")