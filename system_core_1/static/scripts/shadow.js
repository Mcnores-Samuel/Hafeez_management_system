// script.js
const dash = document.querySelector(".dash")
const sidebar = document.querySelector(".left-sidebar")
const topBar = document.querySelector(".heading")
const main = document.querySelector(".main")
const products = document.querySelector(".top_products")

let resizeClasses = ["resize", "topBar", "main-resize", "shift"]
let class_keys = ["size", "top", "main", "unshift"]

window.addEventListener('scroll', () => {
  if (window.scrollY > 10) {
    topBar.style.boxShadow = "3px 3px 7px grey"
  }
  else{
    topBar.style.boxShadow = "none"
  }
});

const resize = () => {
  if (localStorage.getItem(class_keys[0]) === "true" &&
  localStorage.getItem(class_keys[1]) === "true" &&
  localStorage.getItem(class_keys[2]) === "true" &&
  localStorage.getItem(class_keys[3]) === "true")
  {
    sidebar.classList.add(resizeClasses[0]);
    topBar.classList.add(resizeClasses[1]);
    main.classList.add(resizeClasses[2]);
    products.classList.add(resizeClasses[3]);
  }
  dash.addEventListener("click", ()=>{
    sidebar.classList.toggle(resizeClasses[0])
    topBar.classList.toggle(resizeClasses[1])
    main.classList.toggle(resizeClasses[2])
    products.classList.toggle(resizeClasses[3])
    localStorage.setItem(class_keys[0], sidebar.classList.contains(resizeClasses[0]))
    localStorage.setItem(class_keys[1], topBar.classList.contains(resizeClasses[1]))
    localStorage.setItem(class_keys[2], main.classList.contains(resizeClasses[2]))
    localStorage.setItem(class_keys[3], products.classList.contains(resizeClasses[3]))
  });

}
resize();
