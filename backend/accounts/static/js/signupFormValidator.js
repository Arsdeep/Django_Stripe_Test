const form = document.querySelector("form");
const username = document.getElementById("id_username");
const email = document.getElementById("id_email");
const organization = document.getElementById("id_organization");
const newOrganization = document.getElementById("id_new_organization");
const password1 = document.getElementById("id_password1");
const password2 = document.getElementById("id_password2");

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

    if (!password1.value) {
        document.getElementById("error-password1").textContent =
            "Password is required.";
        password1.classList.add("is-invalid");
        valid = false;
    } else if (!isStrongPassword(password1.value)) {
        document.getElementById("error-password1").textContent =
            "Password must be at least 8 characters, contain letters, numbers, and a special character.";
        password1.classList.add("is-invalid");
        valid = false;
    }

    if (!password2.value) {
        document.getElementById("error-password2").textContent =
            "Confirm Password is required.";
        password2.classList.add("is-invalid");
        valid = false;
    } else if (
        password1.value &&
        password2.value &&
        password1.value !== password2.value
    ) {
        document.getElementById("error-password2").textContent =
            "Passwords do not match.";
        password2.classList.add("is-invalid");
        valid = false;
    }

    if (!valid) event.preventDefault();
}

form.addEventListener("submit", validateForm);
