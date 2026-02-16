const burger = document.querySelector(".burger");
const mobile_nav = document.getElementById("mobile-nav-list");
const close_btn = document.querySelector(".close_btn");

if (burger && mobile_nav) {
    burger.addEventListener("click", () => {
        mobile_nav.classList.add("active");
    });
}

if (close_btn && mobile_nav) {
    close_btn.addEventListener("click", () => {
        mobile_nav.classList.remove("active");
    });
}

// Close mobile nav when clicking outside
document.addEventListener('click', (e) => {
    if (mobile_nav && mobile_nav.classList.contains('active')) {
        if (!mobile_nav.contains(e.target) && !burger.contains(e.target)) {
            mobile_nav.classList.remove('active');
        }
    }
});