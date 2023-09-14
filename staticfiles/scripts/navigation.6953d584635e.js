const navBar = document.querySelector('header');
const menu = document.querySelector('.menu');
const navigation = document.querySelector('.heading');
const profile = document.querySelector('.profile');
const settings = document.querySelector('.mobile-set');
const body = document.querySelector('body');

let profileSettings = null;
let isProfileSettingsDisplayed = false; 

profile.addEventListener('click', () => {
  if (!isProfileSettingsDisplayed) {
    profileSettings = document.createElement('div');
    profileSettings.classList.add('profile-settings');
    profileSettings.innerHTML ='<ul><li><i class="bx bx-cog"></i><a href="/cryptic_core_app/profile/">Settings</a></li>\
    <li><i class="bx bx-log-out"></i><a href="/cryptic_core_app/sign_out/">Sign out</a></li></ul>';
    // profileSettings.innerHTML = '';
    navBar.appendChild(profileSettings);
    isProfileSettingsDisplayed = true; // Set the flag to true
  } else {
    // If it's displayed, hide it and remove it from the DOM
    profileSettings.style.display = 'none';
    navBar.removeChild(profileSettings);
    isProfileSettingsDisplayed = false; // Set the flag to false
    profileSettings = null; // Reset the profileSettings variable
  }
});

// Function to close the menu
function closeMenu () {
  navigation.classList.remove('dropmenu');
  profile.style.display = 'flex';
  settings.style.display = 'none';
}

window.addEventListener('scroll', () => {
  if (window.scrollY > 10) {
    navBar.style.boxShadow = "3px 3px 7px grey"
  }
  else{
    navBar.style.boxShadow = "none"
  }
});

// Event listener to close the menu when clicking outside
window.addEventListener('click', (e) => {
  if (!menu.contains(e.target)) {
    closeMenu();
  }
});

// Event listener to open the menu when clicking on the menu button
menu.addEventListener('click', () => {
  navigation.classList.toggle('dropmenu');

  if (navigation.classList.contains('dropmenu')) {
    profile.style.display = 'none';
    settings.style.display = 'block';
  } else {
    closeMenu();
  }
});

// Event listener to close the menu when scrolling
window.addEventListener('scroll', () => {
  closeMenu();
});

// Event listener to close the menu when resizing the window
window.addEventListener('resize', () => {
  closeMenu();
});
