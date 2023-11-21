$('.copy-button').on('click', function() {
    const textToCopy = $('.text-to-copy').text();
    const textarea = $('<textarea>').val(textToCopy);
    
    $('body').append(textarea);
    textarea.select();
    document.execCommand('copy');
    textarea.remove();
    
    $(this).text('Copied!');
});