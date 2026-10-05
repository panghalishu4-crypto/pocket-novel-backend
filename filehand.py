myf = open("isfile.txt", "w")
myf.write("i am testing it")
myf.close()
print("file bn gai")

def add_note():
    note = input("Apna note likhiye: ")
    with open("notes.txt", "a") as f:
        f.write(note + "\n")
    print("✅ Note save ho gaya!\n")

def view_notes():
    try:
        with open("notes.txt", "r") as f:
            content = f.read()
            print("\n--- AAPKE SAVED NOTES ---")
            print(content if content else "File khali hai!")
            print("-------------------------\n")
    except FileNotFoundError:
        print("❌ Koi note nahi mila!\n")

def search_note():
    search_word = input("Kya dhoondhna chahte hain?: ").lower()
    try:
        with open("notes.txt", "r") as f:
            lines = f.readlines()
            found = False
            print("\n--- SEARCH RESULTS ---")
            for note in lines:
                if search_word in note.lower():
                    print("👉 " + note.strip())
                    found = True
            if not found:
                print("❌ Is naam ka koi note nahi mila.")
            print("----------------------\n")
    except FileNotFoundError:
        print("❌ Pehle koi note add kijiye!\n")

def clear_all_notes():
    confirm = input("⚠️ Kya aap SARE notes delete karna chahte hain? (y/n): ")
    if confirm.lower() == "y":
        with open("notes.txt", "w") as f:
            pass
        print("🗑️ Saare notes delete ho gaye!\n")

# Main Menu
while True:
    print("=== ADVANCED NOTES SAVER ===")
    print("1. Naya Note Likhein")
    print("2. Saare Notes Dekhein")
    print("3. Note Search Karein")
    print("4. Saare Notes Delete (Clear) Karein")
    print("5. App Band Karein")
    
    choice = input("Option chunein (1-5): ")
    
    if choice == "1":
        add_note()
    elif choice == "2":
        view_notes()
    elif choice == "3":
        search_note()
    elif choice == "4":
        clear_all_notes()
    elif choice == "5":
        print("App band ho gaya. Bye!")
        break
    else:
        print("Galat option!\n")