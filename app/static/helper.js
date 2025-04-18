const burger = document.querySelector(".burger");
const mobile_nav = document.getElementById("mobile-nav-list");

burger.addEventListener("click", () => {
    mobile_nav.classList.add("active");
});

const close_btn = document.querySelector(".close_btn");
close_btn.addEventListener("click", () => {
    mobile_nav.classList.remove("active");
})