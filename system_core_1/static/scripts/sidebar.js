const folder = $('.topbar-wrapper');
const sidebar = $('.sidebar');
const wrapper = $('.wrapper');
const main = $('.presentaion');
const localStorageKey = 'sidebarResized';

// Function to apply the user's preference for the sidebar state
function applySidebarPreference() {
  const isSidebarResized = localStorage.getItem(localStorageKey) === 'true';

  if (isSidebarResized) {
    $('.text').hide();
    sidebar.addClass('resize');
    wrapper.addClass('resize');
    main.toggleClass('presentaion-resize');
  } else {
    main.removeClass('presentaion-resize');
  }
}

// Check the user's preference after the document is fully loaded
$(document).ready(() => {
  applySidebarPreference();
});

folder.on('click', () => {
  $('.text').toggle();
  sidebar.toggleClass('resize');
  wrapper.toggleClass('resize');
  main.toggleClass('presentaion-resize');

  // Store the user's preference for the sidebar state
  localStorage.setItem(localStorageKey, sidebar.hasClass('resize'));
});

// Adjust the width dynamically if needed
$(window).on('resize', () => {
  const windowWidth = $(window).width();
  const breakpoint = 300; // Adjust the breakpoint as needed

  if (windowWidth < breakpoint) {
    // Remove 'resize' class on smaller screens
    sidebar.removeClass('resize');
    wrapper.removeClass('resize');
    main.toggleClass('presentaion-resize');
  } else {
    // Add 'resize' class on larger screens
    if (localStorage.getItem(localStorageKey) === 'true') {
      sidebar.addClass('resize');
      wrapper.addClass('resize');
      main.toggleClass('presentaion-resize');
    }
  }
});


$(document).ready(function() {
  // Get the current page URL path
  const currentPath = window.location.pathname;

  // Select all navigation links
  $(".navbar-nav .nav-item").each(function() {
      // Check if the href matches the current path
      if ($(this).find('a').attr('href') === currentPath) {
          // Add the active class to the parent list item
          console.log($(this).find('a').attr('href'));
          $(this).addClass('active');
      }
  });
});
