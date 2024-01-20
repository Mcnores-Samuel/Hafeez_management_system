function copyText(elementId) {
    // Get the text from the span
    let textToCopy = document.querySelector("#"+elementId).innerText;
    let textcontainer = document.querySelector("#"+elementId);

    let textarea = document.createElement('textarea');
    textarea.innerText = textToCopy;
    document.body.appendChild(textarea);

    textarea.select();
    textarea.focus();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    textcontainer.classList.add('text-success');
    textcontainer.innerText = "Copied!";
    setTimeout(function(){
        textcontainer.innerText = textToCopy;
    }, 1000);
}