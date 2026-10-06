const BASE_URL = "https://pocket-novel-backend.onrender.com";
let allNovelsData = [];

// Get user info from localStorage safely
const userInfo = JSON.parse(localStorage.getItem("user_info")) || { user_id: null, username: "Guest", coins: 0 };

document.addEventListener("DOMContentLoaded", () => {
  setupHeader();
  
  // Restore active tab state
  const savedTab = localStorage.getItem("active_tab") || "reading-tab";
  const targetNav = document.querySelector(`.nav-item[data-tab="${savedTab}"]`) || document.querySelector('.nav-item');
  switchTab(savedTab, targetNav);

  fetchNovels();
});

// Setup User Header & Profile Info
function setupHeader() {
  if (!userInfo || !userInfo.username) {
    window.location.href = "index.html"; // Redirect if not logged in
    return;
  }

  updateUserCoinsUI(userInfo.coins);
  const userNameEl = document.getElementById("profile-username");
  if (userNameEl) userNameEl.innerText = userInfo.username;
}

function updateUserCoinsUI(coins) {
  document.getElementById("coins-display").innerText = coins;
  const profileCoins = document.getElementById("profile-coins");
  if (profileCoins) profileCoins.innerText = coins;
  
  userInfo.coins = coins;
  localStorage.setItem("user_info", JSON.stringify(userInfo));
}

// Tab Switching Handler
function switchTab(tabId, element) {
  document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));

  const targetTab = document.getElementById(tabId);
  if (targetTab) targetTab.classList.add('active');
  if (element) element.classList.add('active');
  
  localStorage.setItem("active_tab", tabId);

  if (tabId === 'library-tab') {
    loadLibraryData('recent');
  }
}

function logout() {
  localStorage.clear();
  window.location.href = "index.html";
}

// Fetch and Display All Novels
async function fetchNovels() {
  try {
    const response = await fetch(`${BASE_URL}/all-novels`);
    const data = await response.json();
    const container = document.getElementById("novels-list");

    if (data.novels && data.novels.length > 0) {
      allNovelsData = data.novels;
      renderNovelsList(allNovelsData, container);
    } else {
      container.innerHTML = "<p style='color: #b8c1ec;'>No novels available yet. Use Write Tab!</p>";
    }
  } catch (err) {
    const container = document.getElementById("novels-list");
    if (container) container.innerText = "Failed to load novels!";
  }
}

function renderNovelsList(novels, container) {
  if (!container) return;
  container.innerHTML = novels.map(novel => `
    <div class="novel-card">
      <img src="${novel.cover_image_url || 'https://via.placeholder.com/300x400?text=No+Cover'}" class="novel-thumbnail" alt="Cover">
      <div class="novel-details">
        <div class="novel-title">${novel.title}</div>
        <div class="novel-meta">
          <span>✍️ ${novel.author_name}</span>
          <span>👁️ ${novel.views || 0}</span>
        </div>
        <div class="card-actions">
          <div class="action-badge" onclick="toggleLike(${novel.id})">❤️ ${novel.likes_count || 0}</div>
          <div class="action-badge" onclick="toggleBookmark(${novel.id})">🔖 Save</div>
        </div>
        <button class="view-btn" onclick="window.location.href='reader.html?novel_id=${novel.id}'">📖 Read Novel</button>
      </div>
    </div>
  `).join('');
}

// Like Feature
async function toggleLike(novelId) {
  try {
    const res = await fetch(`${BASE_URL}/toggle-like`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userInfo.user_id, novel_id: novelId })
    });
    const data = await res.json();
    if (data.status === "success") {
      fetchNovels();
    }
  } catch (err) {
    console.error("Like error", err);
  }
}

// Bookmark Feature
async function toggleBookmark(novelId) {
  try {
    const res = await fetch(`${BASE_URL}/toggle-bookmark`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userInfo.user_id, novel_id: novelId })
    });
    const data = await res.json();
    alert(data.action === "bookmarked" ? "🔖 Bookmarked successfully!" : "❌ Removed from bookmarks");
  } catch (err) {
    console.error("Bookmark error", err);
  }
}

// Library Management (Recent Reads, Bookmarks, My Writes)
async function loadLibraryData(type, btnElement) {
  if (btnElement) {
    document.querySelectorAll('.library-btn').forEach(b => b.classList.remove('active'));
    btnElement.classList.add('active');
  }

  const container = document.getElementById("library-content-list");
  if (!container) return;
  container.innerHTML = "<p style='color: #b8c1ec; text-align: center;'>Loading library...</p>";

  try {
    if (type === 'writes') {
      const res = await fetch(`${BASE_URL}/writer/novels/${userInfo.user_id}`);
      const data = await res.json();
      if (data.novels && data.novels.length > 0) {
        container.innerHTML = data.novels.map(n => `
          <div class="novel-card">
            <img src="${n.cover_image_url}" class="novel-thumbnail">
            <div class="novel-details">
              <div class="novel-title">${n.title}</div>
              <div class="novel-meta">Views: ${n.views}</div>
              <button class="view-btn" onclick="window.location.href='reader.html?novel_id=${n.id}'">✏️ Manage / View</button>
            </div>
          </div>
        `).join('');
      } else {
        container.innerHTML = "<p style='color: #b8c1ec; text-align: center;'>You haven't written any novels yet.</p>";
      }
    } else {
      const res = await fetch(`${BASE_URL}/user/library/${userInfo.user_id}`);
      const data = await res.json();
      
      if (type === 'recent') {
        const list = data.recent_reads || [];
        if (list.length > 0) {
          container.innerHTML = list.map(item => `
            <div class="novel-card">
              <img src="${item.cover_image_url}" class="novel-thumbnail">
              <div class="novel-details">
                <div class="novel-title">${item.novel_title}</div>
                <div class="novel-meta">Ch ${item.last_chapter_number}: ${item.last_chapter_title}</div>
                <button class="view-btn" onclick="window.location.href='reader.html?novel_id=${item.novel_id}'">📖 Continue Reading</button>
              </div>
            </div>
          `).join('');
        } else {
          container.innerHTML = "<p style='color: #b8c1ec; text-align: center;'>No recent reads found.</p>";
        }
      } else if (type === 'bookmarks') {
        const list = data.bookmarks || [];
        if (list.length > 0) {
          container.innerHTML = list.map(item => `
            <div class="novel-card">
              <img src="${item.cover_image_url}" class="novel-thumbnail">
              <div class="novel-details">
                <div class="novel-title">${item.novel_title}</div>
                <div class="novel-meta">By ${item.author_name}</div>
                <button class="view-btn" onclick="window.location.href='reader.html?novel_id=${item.novel_id}'">📖 Read Novel</button>
              </div>
            </div>
          `).join('');
        } else {
          container.innerHTML = "<p style='color: #b8c1ec; text-align: center;'>No bookmarks saved.</p>";
        }
      }
    }
  } catch (err) {
    container.innerHTML = "<p style='color: #ff4b2b; text-align: center;'>Failed to load library data.</p>";
  }
}

function switchLibraryTab(type, btn) {
  loadLibraryData(type, btn);
}

// Publish Novel Form Handler (Updated to save Chapter 1 from Quill Editor)
async function publishNovel(e) {
  e.preventDefault();
  console.log("🚀 Publish button is click!");

  const payload = {
    title: document.getElementById("novel-title-input").value,
    author_name: document.getElementById("novel-author-input").value,
    genre: document.getElementById("novel-genre-input").value,
    cover_image_url: coverUrl !== "" ? coverUrl : "https://via.placeholder.com/300x400?text=No+Cover",
    access_type: document.getElementById("novel-access-input").value,
    description: document.getElementById("novel-desc-input").value,
    author_id: userInfo.user_id
  };
  console.log("📦 Payload data:", payload);

  try {
    const res = await fetch(`${BASE_URL}/publish-novel`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    console.log("🌐 Server response (/publish-novel):", data);

    if (res.ok && data.status === "success") {
      const novelId = data.novel_id;

      const chapterContent = quill ? quill.root.innerHTML : "<p>Chapter 1 Content</p>";
      const chapterPayload = {
        novel_id: novelId,
        chapter_number: 1,
        chapter_title: "Chapter 1: Beginning",
        content: chapterContent,
        is_locked: 0
      };

      const chRes = await fetch(`${BASE_URL}/add-chapter`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(chapterPayload)
      });
      const chData = await chRes.json();
      console.log("🌐 Server response (/add-chapter):", chData);

      if (chRes.ok && chData.status === "success") {
        alert("🎉 Novel & Chapter 1 Published Successfully!");
        document.getElementById("publish-form").reset();
        if (quill) quill.setContents([]);
        fetchNovels();
        switchTab('reading-tab', document.querySelector('.nav-item'));
      } else {
        alert("Novel created, but failed to save Chapter 1!");
      }
    } else {
      alert("Failed to publish novel: " + (data.detail || "Unknown error"));
    }
  } catch (err) {
    console.error("❌ Catch error:", err);
    alert("Server error during publish!");
  }
}

// Claim Reward Coins
function claimReward(amount, type) {
  let currentCoins = parseInt(userInfo.coins || 0);
  currentCoins += amount;
  updateUserCoinsUI(currentCoins);
  alert(`🎉 Reward Claimed! +${amount} Coins added for ${type}.`);
}

// Real-time Search Filter
const searchInput = document.getElementById("search-input");
if (searchInput) {
  searchInput.addEventListener("input", (e) => {
    const query = e.target.value.toLowerCase().trim();
    const searchContainer = document.getElementById("search-results-grid");
    
    const filtered = allNovelsData.filter(n => 
      n.title.toLowerCase().includes(query) || 
      n.author_name.toLowerCase().includes(query) || 
      n.genre.toLowerCase().includes(query)
    );
    renderNovelsList(filtered, searchContainer);
  });
}