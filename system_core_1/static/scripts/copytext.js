showNotification = require('./data_updates.js').showNotification;


function copyText(elementId) {
    // Get the text from the span
    let textToCopy = document.querySelector("#"+elementId).innerText;

    // Create a temporary textarea element
    let textarea = document.createElement('textarea');
    textarea.value = textToCopy;
    document.body.appendChild(textarea);

    // Select the text and copy it
    textarea.select();
    document.execCommand('copy');

    // Remove the temporary textarea
    document.body.removeChild(textarea);
    showNotification(textToCopy + ' copied!', 'success');

}