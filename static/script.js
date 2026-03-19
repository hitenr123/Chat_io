function toggleForm() {
  const login = document.getElementById("loginForm");
  const register = document.getElementById("registerForm");

  login.classList.toggle("active");
  register.classList.toggle("active");
}


// REGISTER
document.getElementById("registerForm").addEventListener("submit", async function(e){
  e.preventDefault();

  const username = document.querySelector("#registerForm input[type='text']").value;
  const email = document.querySelector("#registerForm input[type='email']").value;
  const password = document.querySelector("#registerForm input[type='password']").value;

  const res = await fetch("/register",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({username,email,password})
  });

  const data = await res.json();

  if(data.status==="success"){
    alert("Account created!");
    toggleForm();
  }else{
    alert("Username already exists");
  }
});


// LOGIN
document.getElementById("loginForm").addEventListener("submit", async function(e){
  e.preventDefault();

  const username = document.querySelector("#loginForm input[type='text']").value;
  const password = document.querySelector("#loginForm input[type='password']").value;

  const res = await fetch("/login",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({username,password})
  });

  const data = await res.json();

  if(data.status==="success"){
    alert("Login successful");
    window.location.href="/dashboard";
  }else{
    alert("Invalid login");
  }
});