// Render ka Live API URL (Apna Render URL yahan paste karein)
const BASE_URL = "https://pocket-novel-backend.onrender.com"; 

let isLoginMode = true;

function toggleForm() {
    isLoginMode = !isLoginMode;
    
    const subTitle = document.getElementById("sub-title");
    const submitBtn = document.getElementById("submit-btn");
    const toggleMsg = document.getElementById("toggle-msg");
    const toggleLink = document.getElementById("toggle-link");
    const message = document.getElementById("message");

    message.innerText = "";

    if (isLoginMode) {
        subTitle.innerText = "Sign in to read your favorite novels";
        submitBtn.innerText = "Login";
        toggleMsg.innerText = "Don't have an account?";
        toggleLink.innerText = "Sign Up";
    } else {
        subTitle.innerText = "Create a new account to get started";
        submitBtn.innerText = "Sign Up";
        toggleMsg.innerText = "Already have an account?";
        toggleLink.innerText = "Login";
    }
}

async function handleSubmit() {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const message = document.getElementById("message");

    if (!email || !password) {
        message.className = "error";
        message.innerText = "Please fill all fields!";
        return;
    }

    message.className = "";
    message.innerText = "Connecting to live server...";

    const endpoint = isLoginMode ? "/login" : "/signup";

    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email: email, password: password })
        });

        const data = await response.json();

        if (response.ok) {
            message.className = "success";
            if (isLoginMode) {
                message.innerText = "Login Successful! 🎉";
                // JWT Token ko browser local storage mein save karte hain
                if (data.access_token) {
                    localStorage.setItem("token", data.access_token);
                }
            } else {
                message.innerText = "Account Created Successfully! Please Login now.";
                toggleForm();
            }
        } else {
            message.className = "error";
            message.innerText = data.detail || "Something went wrong!";
        }
    } catch (error) {
        message.className = "error";
        message.innerText = "Server Error or Render is waking up from sleep. Try again in 30 sec.";
    }
}