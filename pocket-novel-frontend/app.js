const BASE_URL = "https://pocket-novel-backend.onrender.com";
let isLoginMode = true;

// Toggle between Login & Signup
function toggleForm() {
  isLoginMode = !isLoginMode;

  const subTitle = document.getElementById("sub-title");
  const emailGroup = document.getElementById("email-group");
  const submitBtn = document.getElementById("submit-btn");
  const toggleMsg = document.getElementById("toggle-msg");
  const toggleLink = document.getElementById("toggle-link");
  const bonusTag = document.getElementById("bonus-tag");
  const message = document.getElementById("message");

  if (message) message.innerText = "";

  if (isLoginMode) {
    subTitle.innerText = "Sign in to read your favorite novels";
    emailGroup.style.display = "none";
    if (bonusTag) bonusTag.style.display = "none";
    submitBtn.innerText = "Login";
    toggleMsg.innerText = "Don't have an account?";
    toggleLink.innerText = "Sign Up";
  } else {
    subTitle.innerText = "Create an account to start reading";
    emailGroup.style.display = "block";
    if (bonusTag) bonusTag.style.display = "inline-block";
    submitBtn.innerText = "Sign Up";
    toggleMsg.innerText = "Already have an account?";
    toggleLink.innerText = "Login";
  }
}

// Handle Login & Signup Submit
async function handleSubmit() {
  const usernameInput = document.getElementById("username").value.trim();
  const passwordInput = document.getElementById("password").value.trim();
  const emailInput = document.getElementById("email") ? document.getElementById("email").value.trim() : "";
  const message = document.getElementById("message");
  const submitBtn = document.getElementById("submit-btn");

  if (!usernameInput || !passwordInput) {
    message.className = "error";
    message.innerText = "Please fill in all required fields!";
    return;
  }

  const endpoint = isLoginMode ? "/login" : "/signup";
  const payload = isLoginMode 
    ? { username: usernameInput, password: passwordInput }
    : { username: usernameInput, email: emailInput, password: passwordInput };

  try {
    submitBtn.disabled = true;
    submitBtn.innerText = "Processing...";

    const res = await fetch(`${BASE_URL}${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (res.ok) {
      message.className = "success";
      message.innerText = isLoginMode ? "Login Successful! Redirecting..." : "Account created! 100 Coins credited. Redirecting...";

      // Extract user info correctly for both Login and Signup responses
      let userInfo = {};
      if (isLoginMode && data.user_info) {
        userInfo = {
          user_id: data.user_info.user_id,
          username: data.user_info.username,
          coins: data.user_info.coins,
          profile_pic: data.user_info.profile_pic
        };
        if (data.access_token) {
          localStorage.setItem("access_token", data.access_token);
        }
      } else {
        userInfo = {
          user_id: data.user_id,
          username: usernameInput,
          coins: data.coins || 100
        };
      }

      localStorage.setItem("user_info", JSON.stringify(userInfo));

      setTimeout(() => {
        window.location.href = "dashboard.html";
      }, 1200);

    } else {
      message.className = "error";
      message.innerText = data.detail || data.message || "Authentication failed!";
      submitBtn.disabled = false;
      submitBtn.innerText = isLoginMode ? "Login" : "Sign Up";
    }
  } catch (err) {
    message.className = "error";
    message.innerText = "Server connection error! Please try again later.";
    submitBtn.disabled = false;
    submitBtn.innerText = isLoginMode ? "Login" : "Sign Up";
  }
}

// Auto Redirect if User Already Logged In
document.addEventListener("DOMContentLoaded", () => {
  const userInfo = localStorage.getItem("user_info");
  const currentPath = window.location.pathname;

  if (userInfo && (currentPath.endsWith("index.html") || currentPath === "/" || currentPath.endsWith("/"))) {
    window.location.href = "dashboard.html";
  }
});