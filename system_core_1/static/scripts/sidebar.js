const folder = $('.topbar-wrapper')

folder.on('click', function () {
    folder.toggleClass('active');
    alert('clicked')
});