function save_contract_number() {
  const form = document.querySelector('.contract_number_form');
  const formData = new FormData(form);

  fetch('/cryptic_core_app/add_contract_number/', {
      method: 'POST',
      body: formData
  })
  .then(response => response.json())
  .then(data => {
      form.reset();
  })
  .catch(error => {
    console.error(error);
});
}