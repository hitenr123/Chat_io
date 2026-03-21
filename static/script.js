function toggleForm() {
  const login = document.getElementById("loginForm");
  const register = document.getElementById("registerForm");

  login.classList.toggle("active");
  register.classList.toggle("active");
}

function showPopup(message, type) {
  const overlay = document.getElementById("popupOverlay");
  const popup = overlay.querySelector(".popup");
  const text = document.getElementById("popupText");

  text.innerText = message;

  popup.classList.remove("success", "error");

  if (type === "success") {
    popup.classList.add("success");
  } else {
    popup.classList.add("error");
  }

  overlay.style.display = "flex";

  setTimeout(() => {
    overlay.style.display = "none";
  }, 2500);
}

// REGISTER
document
  .getElementById("registerForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = this.querySelector("input[name='username']").value;
    const email = this.querySelector("input[name='email']").value;
    const password = this.querySelector("input[name='password']").value;

    const res = await fetch(
      "https://web-production-3a7ea.up.railway.app/register",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          email: email,
          password: password,
        }),
      },
    );

    const data = await res.json();
    console.log(data);
    if (data.status === "success") {
      showPopup("Registration Successful 🎉", "success");
    } else {
      showPopup("Registration Failed ❌", "error");
    }
  });

// LOGIN
document
  .getElementById("loginForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = this.querySelector("input[name='username']").value;
    const password = this.querySelector("input[name='password']").value;

    const res = await fetch(
      "https://web-production-3a7ea.up.railway.app/login",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      },
    );

    const data = await res.json();
    console.log(data);
    if (data.status === "success") {
      showPopup("Login Successful 🎉", "success");
    } else {
      showPopup("Invalid Username or Password ❌", "error");
    }
  });
