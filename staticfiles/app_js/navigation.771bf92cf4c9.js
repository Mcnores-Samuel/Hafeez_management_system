const navBar = document.querySelector("header");
const menu = document.querySelector(".menu");
const navigation = document.querySelector('.heading');
const profile = document.querySelector('.profile');
const settings = document.querySelector('.settings');
const body = document.querySelector("body");

// Function to close the menu
function closeMenu() {
  navigation.classList.remove('dropmenu');
  profile.style.display = 'block'; // Display the profile
  settings.style.display = 'none'; // Hide the settings
}

// Event listener to close the menu when clicking outside
window.addEventListener("click", (e) => {
  if (!menu.contains(e.target)) {
    closeMenu();
  }
});

// Event listener to open the menu when clicking on the menu button
menu.addEventListener('click', () => {
  navigation.classList.toggle('dropmenu');
  if (navigation.classList.contains('dropmenu')) {
    profile.style.display = 'none'; // Hide the profile
    settings.style.display = 'block'; // Display the settings
    navigation.classList.add('open'); // Add 'open' class for animation
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