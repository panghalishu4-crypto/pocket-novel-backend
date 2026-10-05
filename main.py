import sqlite3
import jwt
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Har frontend website/app ko access allow karega
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Security Settings
SECRET_KEY = "my_super_secret_pocket_novel_key_123"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 1. Database Initialization
def init_db():
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            hashed_password TEXT,
            coins INTEGER DEFAULT 100
        )
    ''')
    
    # Novels Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS novels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author_name TEXT,
            genre TEXT
        )
    ''')
    
    # Chapters Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            novel_id INTEGER,
            chapter_number INTEGER,
            chapter_title TEXT,
            content TEXT,
            is_locked INTEGER DEFAULT 0,
            coin_price INTEGER DEFAULT 10
        )
    ''')
    
    # Unlocked Chapters Tracker
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS unlocked_chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            chapter_id INTEGER,
            UNIQUE(user_id, chapter_id)
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()


# Pydantic Schemas
class SignupSchema(BaseModel):
    username: str
    email: str
    password: str

class LoginSchema(BaseModel):
    username: str
    password: str

class NovelSchema(BaseModel):
    title: str
    author_name: str
    genre: str

class ChapterSchema(BaseModel):
    novel_id: int
    chapter_number: int
    chapter_title: str
    content: str

class UnlockSchema(BaseModel):
    user_id: int
    chapter_id: int

class RechargeSchema(BaseModel):
    user_id: int
    coins_to_add: int


# Security Helpers
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 2. AUTH APIs
@app.post("/signup")
def signup(user: SignupSchema):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    hashed_pwd = hash_password(user.password)
    try:
        cursor.execute('''
            INSERT INTO users (username, email, hashed_password)
            VALUES (?, ?, ?)
        ''', (user.username, user.email, hashed_pwd))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return {
            "status": "success", 
            "message": "User registered successfully!", 
            "user_id": user_id,
            "welcome_bonus_coins": 100
        }
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Username or Email already exists!")

@app.post("/login")
def login(user: LoginSchema):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, hashed_password, coins FROM users WHERE username = ?", (user.username,))
    db_user = cursor.fetchone()
    conn.close()
    
    if not db_user or not verify_password(user.password, db_user[2]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_access_token({"user_id": db_user[0], "username": db_user[1]})
    return {
        "status": "success",
        "message": "Login successful!",
        "access_token": token,
        "token_type": "bearer",
        "user_info": {
            "user_id": db_user[0],
            "username": db_user[1],
            "coins": db_user[3]
        }
    }


# 3. USER PROFILE & WALLET RECHARGE APIs
@app.get("/user/profile/{user_id}")
def get_user_profile(user_id: int):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, coins FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return {
        "status": "success",
        "profile": {
            "user_id": user[0],
            "username": user[1],
            "email": user[2],
            "coin_balance": user[3]
        }
    }

@app.post("/recharge-wallet")
def recharge_wallet(data: RechargeSchema):
    if data.coins_to_add <= 0:
        raise HTTPException(status_code=400, detail="Coin amount must be greater than 0")
        
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT coins FROM users WHERE id = ?", (data.user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
        
    current_coins = user[0]
    new_balance = current_coins + data.coins_to_add
    
    cursor.execute("UPDATE users SET coins = ? WHERE id = ?", (new_balance, data.user_id))
    conn.commit()
    conn.close()
    
    return {
        "status": "success",
        "message": f"Successfully added {data.coins_to_add} coins to wallet!",
        "updated_balance": new_balance
    }


# 4. WRITER APIs
@app.post("/publish-novel")
def publish_novel(novel: NovelSchema):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO novels (title, author_name, genre)
        VALUES (?, ?, ?)
    ''', (novel.title, novel.author_name, novel.genre))
    conn.commit()
    novel_id = cursor.lastrowid
    conn.close()
    return {"status": "success", "message": "Novel created successfully!", "novel_id": novel_id}

@app.post("/add-chapter")
def add_chapter(chapter: ChapterSchema):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    
    is_locked = 0 if chapter.chapter_number <= 2 else 1
    
    cursor.execute('''
        INSERT INTO chapters (novel_id, chapter_number, chapter_title, content, is_locked, coin_price)
        VALUES (?, ?, ?, ?, ?, 10)
    ''', (chapter.novel_id, chapter.chapter_number, chapter.chapter_title, chapter.content, is_locked))
    
    conn.commit()
    chapter_id = cursor.lastrowid
    conn.close()
    
    lock_status = "LOCKED (Requires 10 coins)" if is_locked == 1 else "FREE"
    return {
        "status": "success", 
        "message": f"Chapter added successfully as {lock_status}!", 
        "chapter_id": chapter_id
    }


# 5. PAYWALL & UNLOCK API
@app.post("/unlock-chapter")
def unlock_chapter(data: UnlockSchema):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT coins FROM users WHERE id = ?", (data.user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
        
    user_coins = user[0]
    
    cursor.execute("SELECT coin_price, is_locked FROM chapters WHERE id = ?", (data.chapter_id,))
    chapter = cursor.fetchone()
    if not chapter:
        conn.close()
        raise HTTPException(status_code=404, detail="Chapter not found")
        
    coin_price = chapter[0]
    
    if user_coins < coin_price:
        conn.close()
        raise HTTPException(status_code=400, detail="Insufficient coins! Please recharge your wallet.")
    
    try:
        new_balance = user_coins - coin_price
        cursor.execute("UPDATE users SET coins = ? WHERE id = ?", (new_balance, data.user_id))
        cursor.execute("INSERT INTO unlocked_chapters (user_id, chapter_id) VALUES (?, ?)", (data.user_id, data.chapter_id))
        
        conn.commit()
        conn.close()
        return {
            "status": "success",
            "message": "Chapter unlocked successfully!",
            "remaining_coins": new_balance
        }
    except sqlite3.IntegrityError:
        conn.close()
        return {"status": "success", "message": "Chapter is already unlocked for this user!"}


# 6. READER APIs
@app.get("/all-novels")
def get_all_novels():
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author_name, genre FROM novels")
    rows = cursor.fetchall()
    conn.close()
    novels_list = [{"id": r[0], "title": r[1], "author_name": r[2], "genre": r[3]} for r in rows]
    return {"status": "success", "novels": novels_list}

@app.get("/novel/{novel_id}/chapters")
def get_novel_chapters(novel_id: int):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, chapter_number, chapter_title, is_locked, coin_price 
        FROM chapters 
        WHERE novel_id = ? 
        ORDER BY chapter_number ASC
    ''', (novel_id,))
    rows = cursor.fetchall()
    conn.close()
    
    chapters_list = [{
        "chapter_id": r[0], 
        "chapter_number": r[1], 
        "chapter_title": r[2],
        "is_locked": bool(r[3]),
        "price": r[4]
    } for r in rows]
    return {"status": "success", "novel_id": novel_id, "chapters": chapters_list}

@app.get("/chapter/{chapter_id}")
def read_chapter(chapter_id: int, user_id: int = 0):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT chapter_number, chapter_title, content, is_locked FROM chapters WHERE id = ?", (chapter_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return {"status": "error", "message": "Chapter not found"}
        
    chapter_number, chapter_title, content, is_locked = row
    
    if is_locked == 0:
        conn.close()
        return {
            "status": "success",
            "chapter_number": chapter_number,
            "chapter_title": chapter_title,
            "content": content,
            "access": "FREE"
        }
    
    cursor.execute("SELECT id FROM unlocked_chapters WHERE user_id = ? AND chapter_id = ?", (user_id, chapter_id))
    unlocked = cursor.fetchone()
    conn.close()
    
    if unlocked:
        return {
            "status": "success",
            "chapter_number": chapter_number,
            "chapter_title": chapter_title,
            "content": content,
            "access": "PURCHASED"
        }
    else:
        return {
            "status": "locked",
            "message": "This chapter is locked! Please unlock it using 10 coins.",
            "chapter_number": chapter_number,
            "chapter_title": chapter_title,
            "content": None
        }