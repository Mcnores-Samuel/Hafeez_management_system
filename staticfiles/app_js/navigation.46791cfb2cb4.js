const navBar = document.querySelector("header")
const menu = document.querySelector(".menu")
const navigation = document.querySelector('.heading')
const profile = document.querySelector('.profile')
const settings = document.querySelector('.settings')
const body = document.querySelector("body")

window.addEventListener("click", ()=>{
  settings.style.display = 'none'
});

window.addEventListener('scroll', () => {
    if (window.scrollY > 10) {
      navBar.style.boxShadow = "3px 3px 7px grey"
    }
    else{
      navBar.style.boxShadow = "none"
    }
  });

let dropDownMenu = () => {
    menu.addEventListener('click', ()=> {
        if (navigation.classList.contains('heading')){
        navigation.classList.toggle('dropmenu')
        }

        if (settings.classList.contains('settings') &&
        profile.classList.contains('profile')) {
          profile.style.display = "none"
          settings.style.display = 'block'
        }
    })
  }

dropDownMenu()