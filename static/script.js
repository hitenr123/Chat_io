function toggleForm() {
  const login = document.getElementById("loginForm");
  const register = document.getElementById("registerForm");

  login.classList.toggle("active");
  register.classList.toggle("active");
}