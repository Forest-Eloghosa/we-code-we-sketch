document.addEventListener("DOMContentLoaded", () => {
    const footerText = document.getElementById("footer-text");
    const currentYear = new Date().getFullYear();

    if (footerText) {
        footerText.innerHTML = `&copy; ${currentYear} We Code We Sketch. All rights reserved.`;
    }

    const menuToggle = document.getElementById("menu-toggle");
    const navList = document.getElementById("nav-list");

    if (menuToggle && navList) {
        menuToggle.addEventListener("click", () => {
            navList.classList.toggle("show");

            const isExpanded = menuToggle.getAttribute("aria-expanded") === "true";
            menuToggle.setAttribute("aria-expanded", String(!isExpanded));
        });
    }
});