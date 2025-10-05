const orgSelect = document.getElementById("id_organization");
const newOrgField = document.getElementById("new-org-field");
const orgSelectField = document.getElementById("org-select-field");
const toggleBtn = document.getElementById("toggle-org-btn");

function showNewOrg() {
    newOrgField.style.display = "block";
    orgSelectField.style.display = "none";
    toggleBtn.textContent = "Select Existing Org";
}

function showOrgSelect() {
    newOrgField.style.display = "none";
    orgSelectField.style.display = "block";
    toggleBtn.textContent = "Enter New Org";
}

toggleBtn.addEventListener("click", () => {
    if (newOrgField.style.display === "none") {
        showNewOrg();
    } else {
        showOrgSelect();
    }
});

// Optional: hide new org input if existing org is selected
orgSelect.addEventListener("change", () => {
    if (orgSelect.value) {
        showOrgSelect();
    }
});