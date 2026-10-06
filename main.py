import sqlite3
import jwt
import bcrypt
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext

app = FastAPI(title="Pocket Novel API")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "my_super_secret_pocket_novel_key_123"
ALGORITHM = "HS256"

def init_db():
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            hashed_password TEXT,
            coins INTEGER DEFAULT 100,
            profile_pic TEXT DEFAULT 'https://via.placeholder.com/150'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS novels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author_name TEXT,
            genre TEXT,
            description TEXT,
            access_type TEXT DEFAULT 'coin_locked',
            author_id INTEGER DEFAULT 0,
            views INTEGER DEFAULT 0
        )
    ''')

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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS unlocked_chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            chapter_id INTEGER,
            UNIQUE(user_id, chapter_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reading_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            novel_id INTEGER,
            last_chapter_id INTEGER,
            last_read_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, novel_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            novel_id INTEGER,
            UNIQUE(user_id, novel_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            novel_id INTEGER,
            UNIQUE(user_id, novel_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            novel_id INTEGER,
            user_id INTEGER,
            username TEXT,
            comment_text TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

init_db()

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
    description: Optional[str] = "No description provided."
    access_type: Optional[str] = "coin_locked" # 'free', 'coin_locked', 'subscription'
    author_id: Optional[int] = 0

class ChapterSchema(BaseModel):
    novel_id: int
    chapter_number: int
    chapter_title: str
    content: str
    is_locked: Optional[int] = None

class ActionSchema(BaseModel):
    user_id: int
    novel_id: int

class UnlockSchema(BaseModel):
    user_id: int
    chapter_id: int

class CommentSchema(BaseModel):
    novel_id: int
    user_id: int
    username: str
    comment_text: str

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(days=7)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/signup")
def signup(user: SignupSchema):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, hashed_password, coins) VALUES (?, ?, ?, 100)",
                       (user.username, user.email, hash_password(user.password)))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return {"status": "success", "message": "Registered successfully!", "user_id": user_id, "coins": 100}
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Username or Email already exists!")

@app.post("/login")
def login(user: LoginSchema):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, hashed_password, coins, profile_pic FROM users WHERE username = ?", (user.username,))
    db_user = cursor.fetchone()
    conn.close()

    if not db_user or not verify_password(user.password, db_user[2]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": db_user[0], "username": db_user[1]})
    return {
        "status": "success",
        "access_token": token,
        "user_info": {"user_id": db_user[0], "username": db_user[1], "coins": db_user[3], "profile_pic": db_user[4]}
    }

@app.get("/user/{user_id}/coins")
def get_user_coins(user_id: int):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT coins FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "coins": row[0]}

@app.get("/all-novels")
def get_all_novels(search: Optional[str] = Query(None)):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    if search:
        query = "%" + search + "%"
        cursor.execute("SELECT id, title, author_name, genre, description, access_type, author_id, views FROM novels WHERE title LIKE ? OR author_name LIKE ? OR genre LIKE ?", (query, query, query))
    else:
        cursor.execute("SELECT id, title, author_name, genre, description, access_type, author_id, views FROM novels")
    rows = cursor.fetchall()
    
    # Get likes and bookmarks count for each novel
    novels_list = []
    for r in rows:
        novel_id = r[0]
        cursor.execute("SELECT COUNT(*) FROM likes WHERE novel_id = ?", (novel_id,))
        likes_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM bookmarks WHERE novel_id = ?", (novel_id,))
        bookmarks_count = cursor.fetchone()[0]

        novels_list.append({
            "id": novel_id,
            "title": r[1],
            "author_name": r[2],
            "genre": r[3],
            "description": r[4],
            "access_type": r[5],
            "author_id": r[6],
            "views": r[7],
            "likes_count": likes_count,
            "bookmarks_count": bookmarks_count
        })
    conn.close()
    return {"status": "success", "novels": novels_list}

@app.post("/publish-novel")
def publish_novel(novel: NovelSchema):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO novels (title, author_name, genre, description, access_type, author_id, views)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0)
    ''', (novel.title, novel.author_name, novel.genre, novel.description, novel.access_type, novel.author_id))
    conn.commit()
    novel_id = cursor.lastrowid
    conn.close()
    return {"status": "success", "message": "Novel created!", "novel_id": novel_id}

@app.get("/writer/novels/{author_id}")
def get_writer_novels(author_id: int):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author_name, genre, description, access_type, views FROM novels WHERE author_id = ?", (author_id,))
    rows = cursor.fetchall()
    conn.close()
    return {"status": "success", "novels": [{"id": r[0], "title": r[1], "author_name": r[2], "genre": r[3], "description": r[4], "access_type": r[5], "views": r[6]} for r in rows]}

@app.post("/add-chapter")
def add_chapter(chapter: ChapterSchema):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()

    # Chapters 1 to 10 are ALWAYS free, 11+ depend on writer setting or default lock
    if chapter.chapter_number <= 10:
        is_locked = 0
    else:
        is_locked = 1 if chapter.is_locked is None else chapter.is_locked

    cursor.execute('''
        INSERT INTO chapters (novel_id, chapter_number, chapter_title, content, is_locked, coin_price)
        VALUES (?, ?, ?, ?, ?, 10)
    ''', (chapter.novel_id, chapter.chapter_number, chapter.chapter_title, chapter.content, is_locked))
    conn.commit()
    chapter_id = cursor.lastrowid
    conn.close()
    return {"status": "success", "message": "Chapter added successfully!", "chapter_id": chapter_id}

@app.get("/novel/{novel_id}/chapters")
def get_novel_chapters(novel_id: int, user_id: int = 0):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    
    # Increment view count when novel chapters are loaded
    cursor.execute("UPDATE novels SET views = views + 1 WHERE id = ?", (novel_id,))
    conn.commit()

    cursor.execute("SELECT id, chapter_number, chapter_title, is_locked, coin_price FROM chapters WHERE novel_id = ? ORDER BY chapter_number ASC", (novel_id,))
    rows = cursor.fetchall()

    unlocked_ids = set()
    if user_id > 0:
        cursor.execute("SELECT chapter_id FROM unlocked_chapters WHERE user_id = ?", (user_id,))
        unlocked_ids = {r[0] for r in cursor.fetchall()}

    conn.close()

    chapters_list = []
    for r in rows:
        ch_num = r[1]
        is_locked = False if ch_num <= 10 else bool(r[3])
        chapters_list.append({
            "chapter_id": r[0],
            "chapter_number": ch_num,
            "chapter_title": r[2],
            "is_locked": is_locked,
            "is_unlocked": r[0] in unlocked_ids,
            "price": r[4]
        })

    return {"status": "success", "novel_id": novel_id, "chapters": chapters_list}

@app.get("/chapter/{chapter_id}")
def read_chapter(chapter_id: int, user_id: int = 0):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT novel_id, chapter_number, chapter_title, content, is_locked FROM chapters WHERE id = ?", (chapter_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Chapter not found")

    novel_id, chapter_number, chapter_title, content, is_locked = row

    if chapter_number <= 10:
        is_locked = 0

    if user_id > 0:
        cursor.execute('''
            INSERT INTO reading_history (user_id, novel_id, last_chapter_id, last_read_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id, novel_id) DO UPDATE SET
                last_chapter_id = excluded.last_chapter_id,
                last_read_at = CURRENT_TIMESTAMP
        ''', (user_id, novel_id, chapter_id))
        conn.commit()

    if is_locked == 0:
        conn.close()
        return {"status": "success", "novel_id": novel_id, "chapter_number": chapter_number, "chapter_title": chapter_title, "content": content, "access": "FREE"}

    cursor.execute("SELECT id FROM unlocked_chapters WHERE user_id = ? AND chapter_id = ?", (user_id, chapter_id))
    unlocked = cursor.fetchone()
    conn.close()

    if unlocked:
        return {"status": "success", "novel_id": novel_id, "chapter_number": chapter_number, "chapter_title": chapter_title, "content": content, "access": "PURCHASED"}
    else:
        return {"status": "locked", "novel_id": novel_id, "chapter_number": chapter_number, "chapter_title": chapter_title, "content": None}

@app.post("/unlock-chapter")
def unlock_chapter(data: UnlockSchema):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()

    cursor.execute("SELECT coins FROM users WHERE id = ?", (data.user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    if user[0] < 10:
        conn.close()
        raise HTTPException(status_code=400, detail="Insufficient coins!")

    try:
        new_balance = user[0] - 10
        cursor.execute("UPDATE users SET coins = ? WHERE id = ?", (new_balance, data.user_id))
        cursor.execute("INSERT INTO unlocked_chapters (user_id, chapter_id) VALUES (?, ?)", (data.user_id, data.chapter_id))
        conn.commit()
        conn.close()
        return {"status": "success", "remaining_coins": new_balance}
    except sqlite3.IntegrityError:
        conn.close()
        return {"status": "success", "message": "Already unlocked"}

@app.post("/toggle-like")
def toggle_like(data: ActionSchema):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM likes WHERE user_id = ? AND novel_id = ?", (data.user_id, data.novel_id))
    liked = cursor.fetchone()
    if liked:
        cursor.execute("DELETE FROM likes WHERE id = ?", (liked[0],))
        status = "unliked"
    else:
        cursor.execute("INSERT INTO likes (user_id, novel_id) VALUES (?, ?)", (data.user_id, data.novel_id))
        status = "liked"
    conn.commit()
    conn.close()
    return {"status": "success", "action": status}

@app.post("/toggle-bookmark")
def toggle_bookmark(data: ActionSchema):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM bookmarks WHERE user_id = ? AND novel_id = ?", (data.user_id, data.novel_id))
    bm = cursor.fetchone()
    if bm:
        cursor.execute("DELETE FROM bookmarks WHERE id = ?", (bm[0],))
        status = "unbookmarked"
    else:
        cursor.execute("INSERT INTO bookmarks (user_id, novel_id) VALUES (?, ?)", (data.user_id, data.novel_id))
        status = "bookmarked"
    conn.commit()
    conn.close()
    return {"status": "success", "action": status}

@app.get("/user/library/{user_id}")
def get_user_library(user_id: int):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    
    # Recent Reads
    cursor.execute('''
        SELECT n.id, n.title, c.id, c.chapter_number, c.chapter_title, rh.last_read_at
        FROM reading_history rh
        JOIN novels n ON rh.novel_id = n.id
        JOIN chapters c ON rh.last_chapter_id = c.id
        WHERE rh.user_id = ? ORDER BY rh.last_read_at DESC
    ''', (user_id,))
    recent_rows = cursor.fetchall()

    # Bookmarks
    cursor.execute('''
        SELECT n.id, n.title, n.author_name, n.genre
        FROM bookmarks b
        JOIN novels n ON b.novel_id = n.id
        WHERE b.user_id = ?
    ''', (user_id,))
    bookmark_rows = cursor.fetchall()

    conn.close()
    return {
        "status": "success",
        "recent_reads": [{"novel_id": r[0], "novel_title": r[1], "last_chapter_id": r[2], "last_chapter_number": r[3], "last_chapter_title": r[4], "last_read_at": r[5]} for r in recent_rows],
        "bookmarks": [{"novel_id": r[0], "novel_title": r[1], "author_name": r[2], "genre": r[3]} for r in bookmark_rows]
    }

@app.post("/add-comment")
def add_comment(comment: CommentSchema):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (novel_id, user_id, username, comment_text) VALUES (?, ?, ?, ?)",
                   (comment.novel_id, comment.user_id, comment.username, comment.comment_text))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Comment added successfully!"}

@app.get("/novel/{novel_id}/comments")
def get_novel_comments(novel_id: int):
    conn = sqlite3.connect("pocket_novel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, username, comment_text, created_at FROM comments WHERE novel_id = ? ORDER BY id DESC", (novel_id,))
    rows = cursor.fetchall()
    conn.close()
    return {"status": "success", "comments": [{"id": r[0], "user_id": r[1], "username": r[2], "comment_text": r[3], "created_at": r[4]} for r in rows]}