function save_contract_number() {
  const form = document.querySelector('.contract_number_form');
  const formData = new FormData(form);

  fetch('/system_core_1/add_contract_number/', {
      method: 'POST',
      body: formData
  })
  .then(response => response.json())
  .then(data => {
      form.reset();
      window.location.href = '/system_core_1/dashboard/';
  })
  .catch(error => {
    console.error(error);
});
}


const textToCopy = document.querySelector('.text-to-copy');
const copyButton = document.querySelector('.copy-button');

copyButton.addEventListener('click', () => {
    const textarea = document.createElement('textarea');
    textarea.value = textToCopy.innerText;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    copyButton.innerText = 'Copied!';
});
