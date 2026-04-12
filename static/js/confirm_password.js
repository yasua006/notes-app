import { main_elem } from "./modules/main_elem_var.js";
const password = main_elem.querySelector("form #password");
const confirm_password = main_elem.querySelector("form #confirm-password");
const validate_password = () => {
    if (password.value !== confirm_password.value) {
        confirm_password.setCustomValidity("Passwords don't match");
    } else {
        confirm_password.setCustomValidity("");
    }
}
const main = () => {
    password.addEventListener("input", () => validate_password());
    confirm_password.addEventListener("input", () => validate_password());
}
main();
