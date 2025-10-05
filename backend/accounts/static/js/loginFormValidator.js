const form = document.getElementById('loginForm');
const username = form.querySelector('input[name="username"]');
const password = form.querySelector('input[name="password"]');

function clearErrors() {
    // Remove previous error messages and invalid classes
    ['username', 'password'].forEach(id => {
        const input = document.getElementById(id);
        const error = document.getElementById(`error-${id}`);
        if (input) input.classList.remove('is-invalid');
        if (error) error.textContent = '';
    });
}

function validateForm(event) {
    clearErrors();
    let valid = true;

    if (!username.value.trim()) {
        document.getElementById('error-username').textContent = "Username is required.";
        username.classList.add('is-invalid');
        valid = false;
    }

    if (!password.value) {
        document.getElementById('error-password').textContent = "Password is required.";
        password.classList.add('is-invalid');
        valid = false;
    }

    if (!valid) event.preventDefault();
}

form.addEventListener('submit', validateForm);
