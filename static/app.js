// document.addEventListener("DOMContentLoaded", () => {
//     const form = document.getElementById("registerForm");
//     const status = document.getElementById("registerStatus");
//     const submitBtn = document.getElementById("submitBtn");

//     if (!form) return;

//     form.addEventListener("submit", async (e) => {
//         e.preventDefault(); 
        
//         // 1. Reset UI
//         status.textContent = "Creating account...";
//         status.className = "form-status";
//         status.style.color = "blue";
//         submitBtn.disabled = true;

//         // 2. Gather Data
//         const formData = new FormData(form);
//         const data = Object.fromEntries(formData.entries());

//         try {
//             // ---------------------------------------------------------
//             // STEP A: REGISTER THE USER
//             // ---------------------------------------------------------
//             const registerResponse = await fetch("http://127.0.0.1:8000/api/register/", {
//                 method: "POST",
//                 headers: { "Content-Type": "application/json" },
//                 body: JSON.stringify(data),
//             });

//             const registerResult = await registerResponse.json();

//             if (registerResponse.ok) {
//                 status.textContent = "Account created. Logging you in...";
                
//                 // ---------------------------------------------------------
//                 // STEP B: AUTOMATICALLY LOGIN
//                 // We reuse the 'data' object (email/password) to hit the login API immediately
//                 // ---------------------------------------------------------
                
//                 // Note: Change '/api/login/' to your actual login URL if different
//                 const loginResponse = await fetch("http://127.0.0.1:8000/api/login/", {
//                     method: "POST",
//                     headers: { "Content-Type": "application/json" },
//                     body: JSON.stringify({
//                         username: data.email, // Django usually expects 'username', so we map email to it
//                         password: data.password
//                     }),
//                 });

//                 if (loginResponse.ok) {
//                     const loginResult = await loginResponse.json();
                    
//                     // 1. Save the Token (if your backend uses Tokens/JWT)
//                     if (loginResult.token) {
//                         localStorage.setItem("auth_token", loginResult.token);
//                     }
//                     if (loginResult.access) {
//                         localStorage.setItem("access_token", loginResult.access); // For JWT
//                     }

//                     // 2. Redirect to the Dashboard/Home instead of Login
//                     status.textContent = "Success! Redirecting...";
//                     status.style.color = "green";
//                     window.location.href = "index.html"; 
//                 } else {
//                     // Fallback: If auto-login fails, send them to the login page manually
//                     console.warn("Auto-login failed", loginResponse);
//                     window.location.href = "login.html";
//                 }

//             } else {
//                 // Handle Registration Errors
//                 status.textContent = registerResult.error || "Registration failed.";
//                 status.style.color = "red";
//                 submitBtn.disabled = false;
//             }

//         } catch (error) {
//             console.error("Network Error:", error);
//             status.textContent = "Could not connect to the server.";
//             status.style.color = "red";
//             submitBtn.disabled = false;
//         }
//     });
// });