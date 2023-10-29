// Load this script after the page has loaded
const categories = document.querySelector('.Categories-icon');
const categoriesMenu = document.querySelector('.Categories-menu');


document.addEventListener("DOMContentLoaded", function () {
  const sections = document.querySelectorAll("li");

  sections.forEach((section) => {
      section.addEventListener("click", function () {
          // Remove "active" class from all sections
          sections.forEach((s) => s.classList.remove("active"));
          // Add "active" class to the clicked section
          section.classList.add("active");
      });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const button = document.querySelector(".scroll-back");

  // Show the button when the user scrolls down 20px from the top of the document
  window.onscroll = function () {
      if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
          button.style.display = "block";
      } else {
          button.style.display = "none";
      }
  };

  // Scroll to the top when the button is clicked
  button.addEventListener("click", function () {
      document.body.scrollTop = 0; // For Safari
      document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE, and Opera
  });
});

categories.addEventListener('click', function() {
  categoriesMenu.classList.toggle('Categories-menu-active');

  if (categoriesMenu.classList.contains('Categories-menu-active')) {
    categories.innerHTML = `<i class='bx bx-chevrons-up bx-fade-up '></i>`
  }
  else {
    categories.innerHTML = `<i class='bx bx-chevrons-down bx-fade-down'></i>`
  }
});