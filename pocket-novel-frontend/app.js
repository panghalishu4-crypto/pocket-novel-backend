// Render ka Live API URL
 const BASE_URL = "https://pocket-novel-backend.onrender.com"; 

let isLoginMode = true;

function toggleForm() {
    isLoginMode = !isLoginMode;
    
    const subTitle = document.getElementById("sub-title");
    const submitBtn = document.getElementById("submit-btn");
    const toggleMsg = document.getElementById("toggle-msg");
    const toggleLink = document.getElementById("toggle-link");
    const emailGroup = document.getElementById("email-group");
    const message = document.getElementById("message");

    message.innerText = "";

    if (isLoginMode) {
        subTitle.innerText = "Sign in to read your favorite novels";
        submitBtn.innerText = "Login";
        toggleMsg.innerText = "Don't have an account?";
        toggleLink.innerText = "Sign Up";
        emailGroup.style.display = "none"; // Hide email field for Login
    } else {
        subTitle.innerText = "Create a new account to get started";
        submitBtn.innerText = "Sign Up";
        toggleMsg.innerText = "Already have an account?";
        toggleLink.innerText = "Login";
        emailGroup.style.display = "block"; // Show email field for Signup
    }
}

async function handleSubmit() {
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const message = document.getElementById("message");

    if (!username || !password || (!isLoginMode && !email)) {
        message.className = "error";
        message.innerText = "Please fill all required fields!";
        return;
    }

    message.className = "";
    message.innerText = "Connecting to live server...";

    const endpoint = isLoginMode ? "/login" : "/signup";
    
    // Exact schema based on backend FastAPI requirement
    const payload = isLoginMode 
        ? { username: username, password: password }
        : { username: username, email: email, password: password };

    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            message.className = "success";
            if (isLoginMode) {
                message.innerText = "Login Successful! 🎉";
                if (data.access_token) {
                    localStorage.setItem("token", data.access_token);
                }
            } else {
                message.innerText = "Account Created Successfully! Please Login now.";
                toggleForm();
            }
        } else {
            message.className = "error";
            if (typeof data.detail === "string") {
                message.innerText = data.detail;
            } else if (Array.isArray(data.detail)) {
                message.innerText = data.detail[0]?.msg || "Validation error!";
            } else {
                message.innerText = "Invalid credentials or request!";
            }
        }
    } catch (error) {
        message.className = "error";
        message.innerText = "Server Error or Render is waking up. Try again!";
    }
}