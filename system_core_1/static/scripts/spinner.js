const loader = document.querySelector('.loader');

window.addEventListener('load', () => {
  loader.classList.add('hide-loader');
});

let slideIndex = 0;
showSlides();
