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


function showNotification(message, type = 'info') {
    const notification = document.querySelector('#notification');
    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.style.display = 'block';

    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}

function recieved() {
    const form = document.querySelector('.recieved_form');
    const formData = new FormData(form);

    fetch('/system_core_1/verify_stock_recieved/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const verified = document.querySelector('.verified');
        showNotification(data.message, 'success');
        verified.innerHTML = `<input type="checkbox" id="checkbox" checked disabled>
        <label for="checkbox" class="checkbox"></label>`;
    })
}

function add_pending() {
    const form = document.querySelector('.sold_form');
    const formData = new FormData(form);

    fetch('/system_core_1/sale_aitel_device/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        form.reset();
        showNotification(data.message, 'success');
    }).catch(error => {
        showNotification(error.message, 'error');
    });
}
