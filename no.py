# 1. Novels Data (Database Proxy)
library = [
    {
        "id": 1,
        "title": "The Alpha King",
        "author": "John Doe",
        "genre": "Romance",
        "is_locked": False,
        "content": "Chapter 1: The forest was quiet when the king arrived..."
    },
    {
        "id": 2,
        "title": "Vampire Secrets",
        "author": "Jane Smith",
        "genre": "Fantasy",
        "is_locked": True,
        "cost": 10,
        "content": "Chapter 1: The castle doors creaked open in the moonlight..."
    }
]

user_coins = 15

# 2. App Welcome Screen
print("=== WELCOME TO POCKET READS ===")
print(f"Aapke paas balance: {user_coins} Coins\n")

# 3. Available Novels Dikhana (Loop)
print("Available Novels:")
for book in library:
    status = "🔒 Locked" if book["is_locked"] else "🔓 Free"
    print(f"[{book['id']}] {book['title']} ({book['genre']}) - {status}")

# 4. User Choice & Logic
choice = int(input("\nKaunsi book padhna chahte hain? (ID type karein 1 ya 2): "))

# Book Search
selected_book = None
for book in library:
    if book["id"] == choice:
        selected_book = book

# Condition Checking
if selected_book:
    if selected_book["is_locked"]:
        if user_coins >= selected_book["cost"]:
            user_coins -= selected_book["cost"]
            print(f"\n🎉 Succesfully unlocked! Remaining Coins: {user_coins}")
            print(f"\n--- {selected_book['title']} ---")
            print(selected_book["content"])
        else:
            print("\n❌ Inefficient Coins! Recharge karein.")
    else:
        print(f"\n--- {selected_book['title']} ---")
        print(selected_book["content"])
else:
    print("\nInvalid choice!")
    