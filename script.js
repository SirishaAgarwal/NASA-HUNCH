
function getUsers() {
  return JSON.parse(localStorage.getItem("users")) || [];
}

function saveUsers(users) {
  localStorage.setItem("users", JSON.stringify(users));
}


function showSignup() {
  document.getElementById("loginPage").classList.add("hidden");
  document.getElementById("signupPage").classList.remove("hidden");
}

function showLogin() {
  document.getElementById("signupPage").classList.add("hidden");
  document.getElementById("loginPage").classList.remove("hidden");
}


function handleSignup() {
  const fullName = document.getElementById("fullName").value.trim();
  const email = document.getElementById("signupEmail").value.trim();
  const password = document.getElementById("signupPassword").value.trim();
  const month = document.getElementById("month").value;
  const day = document.getElementById("day").value;
  const year = document.getElementById("year").value;
  const message = document.getElementById("signupMessage");

  message.style.color = "red";

  if (!fullName || !email || !password || !month || !day || !year) {
    message.textContent = "Please fill in all fields.";
    return;
  }

  const birthDate = new Date(year, month - 1, day);
  const today = new Date();

  let age = today.getFullYear() - birthDate.getFullYear();
  const m = today.getMonth() - birthDate.getMonth();

  if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }

  if (age < 18) {
    message.textContent = "You must be 18 or older to sign up.";
    return;
  }


  let users = getUsers();
  const existingUser = users.find(user => user.email === email);

  if (existingUser) {
    message.textContent = "Account already exists.";
    return;
  }

  const newUser = {
    fullName: fullName,
    email: email,
    password: password,
    dob: `${month}/${day}/${year}`
  };

  users.push(newUser);
  saveUsers(users);

  message.style.color = "lightgreen";
  message.textContent = "Account created! Redirecting to login...";

  setTimeout(() => {
    showLogin();
  }, 1500);
}


function handleLogin() {
  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value.trim();
  const message = document.getElementById("loginMessage");

  message.style.color = "red";

  let users = getUsers();

  const user = users.find(
    user => user.email === email && user.password === password
  );

  if (!user) {
    message.textContent = "Invalid email or password.";
    return;
  }

  localStorage.setItem("loggedInUser", email);

  showDashboard(user);
}


function showDashboard(user) {
  document.getElementById("loginPage").classList.add("hidden");
  document.getElementById("signupPage").classList.add("hidden");
  document.getElementById("dashboard").classList.remove("hidden");

  document.getElementById("welcomeText").innerText =
    "Welcome, " + user.fullName;
}

function logout() {
  localStorage.removeItem("loggedInUser");
  document.getElementById("dashboard").classList.add("hidden");
  document.getElementById("loginPage").classList.remove("hidden");
}


window.onload = function () {

  const month = document.getElementById("month");
  const day = document.getElementById("day");
  const year = document.getElementById("year");

  if (month && day && year) {

    
    let monthPlaceholder = new Option("Month", "", true, true);
    monthPlaceholder.disabled = true;
    month.appendChild(monthPlaceholder);

    const months = [
      "Jan","Feb","Mar","Apr","May","Jun",
      "Jul","Aug","Sep","Oct","Nov","Dec"
    ];

    months.forEach((m, index) => {
      month.appendChild(new Option(m, index + 1));
    });

    let dayPlaceholder = new Option("Day", "", true, true);
    dayPlaceholder.disabled = true;
    day.appendChild(dayPlaceholder);

    for (let i = 1; i <= 31; i++) {
      day.appendChild(new Option(i, i));
    }

    let yearPlaceholder = new Option("Year", "", true, true);
    yearPlaceholder.disabled = true;
    year.appendChild(yearPlaceholder);

    const currentYear = new Date().getFullYear();
    for (let i = currentYear; i >= 1900; i--) {
      year.appendChild(new Option(i, i));
    }
  }


  const loggedInEmail = localStorage.getItem("loggedInUser");

  if (loggedInEmail) {
    const users = getUsers();
    const user = users.find(u => u.email === loggedInEmail);
    if (user) {
      showDashboard(user);
    }
  }
};
