const BASE_URL = "https://pocket-novel-backend.onrender.com";
let currentNovelId = null;
let currentUser = JSON.parse(localStorage.getItem("user_info") || "null");

document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  currentNovelId = urlParams.get("id") || urlParams.get("novel_id");

  if (currentNovelId) {
    loadNovelDetails();
    loadChapterList();
  } else {
    alert("Novel not found!");
    window.location.href = "dashboard.html";
  }
});

// Load Novel Details (Title, Author, Genre, Description)
async function loadNovelDetails() {
  try {
    const res = await fetch(`${BASE_URL}/all-novels`);
    const data = await res.json();
    
    if (data.novels) {
      const novel = data.novels.find(n => n.id == currentNovelId);
      if (novel) {
        const titleEl = document.getElementById("novel-title");
        const authorEl = document.getElementById("novel-author");
        const genreEl = document.getElementById("novel-genre");
        const descEl = document.getElementById("novel-desc");

        if (titleEl) titleEl.innerText = novel.title;
        if (authorEl) authorEl.innerText = `By ${novel.author_name}`;
        if (genreEl) genreEl.innerText = novel.genre;
        if (descEl) descEl.innerText = novel.description;
      }
    }
  } catch (err) {
    console.error("Error loading novel details:", err);
  }
}

// Load Chapter List with Lock / Unlock Status
async function loadChapterList() {
  const userId = currentUser ? (currentUser.user_id || currentUser.id) : 0;
  const chapterListEl = document.getElementById("chapter-list");
  if (!chapterListEl) return;

  try {
    const res = await fetch(`${BASE_URL}/novel/${currentNovelId}/chapters?user_id=${userId}`);
    const data = await res.json();

    if (data.chapters && data.chapters.length > 0) {
      chapterListEl.innerHTML = data.chapters.map(ch => {
        let badge = '<span class="badge free" style="color: #38ef7d; font-weight: bold;">FREE</span>';
        
        if (ch.is_locked) {
          if (ch.is_unlocked) {
            badge = '<span class="badge unlocked" style="color: #00dfd8; font-weight: bold;">UNLOCKED</span>';
          } else {
            badge = `<span class="badge locked" style="color: #ff9a9e; font-weight: bold;">🔒 10 Coins</span>`;
          }
        }

        return `
          <div class="chapter-item" onclick="openChapter(${ch.chapter_id})" style="display: flex; justify-content: space-between; align-items: center; padding: 12px 15px; background: rgba(255,255,255,0.05); margin-bottom: 8px; border-radius: 10px; cursor: pointer; border: 1px solid rgba(255,255,255,0.1); transition: 0.2s;">
            <div>
              <strong style="color: #fff;">Chapter ${ch.chapter_number}:</strong> <span style="color: #b8c1ec;">${ch.chapter_title}</span>
            </div>
            <div>${badge}</div>
          </div>
        `;
      }).join('');
    } else {
      chapterListEl.innerHTML = "<p style='color: #b8c1ec; text-align: center;'>No chapters uploaded yet.</p>";
    }
  } catch (err) {
    console.error("Error loading chapters:", err);
    chapterListEl.innerHTML = "<p style='color: #ff416c; text-align: center;'>Failed to load chapters.</p>";
  }
}

function openChapter(chapterId) {
  window.location.href = `reader.html?novel_id=${currentNovelId}&chapter_id=${chapterId}`;
}