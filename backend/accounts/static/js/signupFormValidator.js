const form = document.querySelector("form");
const username = document.getElementById("id_username");
const email = document.getElementById("id_email");
const organization = document.getElementById("id_organization");
const newOrganization = document.getElementById("id_new_organization");
const password = document.getElementById("id_password");

function isStrongPassword(password) {
    const minLength = 8;
    const hasLetter = /[A-Za-z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password); // new
    const notAllNumeric = /\D/.test(password);

    return (
        password.length >= minLength &&
        hasLetter &&
        hasNumber &&
        hasSpecialChar &&   // enforce special character
        notAllNumeric
    );
}


function clearErrors() {
    document
        .querySelectorAll(".invalid-feedback")
        .forEach((el) => (el.textContent = ""));
    document
        .querySelectorAll(".is-invalid")
        .forEach((el) => el.classList.remove("is-invalid"));
}

function validateForm(event) {
    clearErrors();
    let valid = true;

    if (!username.value.trim()) {
        document.getElementById("error-username").textContent =
            "Username is required.";
        username.classList.add("is-invalid");
        valid = false;
    }

    if (!email.value.trim()) {
        document.getElementById("error-email").textContent =
            "Email is required.";
        email.classList.add("is-invalid");
        valid = false;
    }

    if (!organization.value && !newOrganization.value.trim()) {
        document.getElementById("error-organization").textContent =
            "Existing or New Organization is required.";
        organization.classList.add("is-invalid");
        newOrganization.classList.add("is-invalid");
        valid = false;
    }

    if (!password.value) {
        document.getElementById("error-password").textContent =
            "Password is required.";
        password.classList.add("is-invalid");
        valid = false;
    } else if (!isStrongPassword(password.value)) {
        document.getElementById("error-password").textContent =
            "Password must be at least 8 characters, contain letters, numbers, and a special character.";
        password.classList.add("is-invalid");
        valid = false;
    }

    if (!valid) event.preventDefault();
}

form.addEventListener("submit", validateForm);
