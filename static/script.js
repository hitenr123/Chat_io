function toggleForm() {
  const login = document.getElementById("loginForm");
  const register = document.getElementById("registerForm");

  login.classList.toggle("active");
  register.classList.toggle("active");
}


// REGISTER
document.getElementById("registerForm").addEventListener("submit", async function(e){
  e.preventDefault();

  const username = this.querySelector("input[name='username']").value;
  const email = this.querySelector("input[name='email']").value;
  const password = this.querySelector("input[name='password']").value;

  const res = await fetch("https://web-production-3a7ea.up.railway.app/register",{
    method:"POST",
    headers:{
      "Content-Type":"application/json"
    },
    body:JSON.stringify({
      username,
      email,
      password
    })
  });

  const data = await res.json();
  console.log(data);
});


// LOGIN
document.getElementById("loginForm").addEventListener("submit", async function(e){
  e.preventDefault();

  const username = this.querySelector("input[name='username']").value;
  const password = this.querySelector("input[name='password']").value;

  const res = await fetch("https://web-production-3a7ea.up.railway.app/login",{
    method:"POST",
    headers:{
      "Content-Type":"application/json"
    },
    body:JSON.stringify({
      username,
      password
    })
  });

  const data = await res.json();
  console.log(data);
});