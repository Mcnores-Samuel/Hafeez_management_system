let container = [];
const form = $('#stock_form');
const imei_1 = $('#id_device_imei');
const imei_2 = $('#id_device_imei_2');
const name = $('#id_name');
const cost_price = $('#id_cost_price');
const category = $('#id_category');
const specs = $('#id_spec');
const supplier = $('#id_supplier');
const waitRoom = $('#waiting-room');
const send = $('#submit');
const total = $('#total').text(container.length);
const load = $('#loader')
load.hide()

imei_2.on('change', (e) => {
  e.preventDefault();

  if (imei_1.val().length !== 15 || imei_2.val().length !== 15) {
    const note = '<div class="alert alert-warning alert-dismissible fade show" role="alert">IMEI numbers must be 15 digits long\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>';
    $(note).insertBefore(form);
    setTimeout(() => {
      $('.alert').alert('close');
    }, 5000);
    form.trigger('reset');
    imei_1.focus();
    return;
  }

  if (imei_1.val() === imei_2.val()) {
    const note = '<div class="alert alert-warning alert-dismissible fade show" role="alert">IMEI numbers must be different\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>';
    $(note).insertBefore(form);
    setTimeout(() => {
      $('.alert').alert('close');
    }, 5000);
    form.trigger('reset');
    imei_1.focus();
    return;
  }

  if (container.length === 30) {
    const note = '<div class="alert alert-warning alert-dismissible fade show" role="alert">Maximum number of items scanned\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>';
    $(note).insertBefore(form);
    setTimeout(() => {
      $('.alert').alert('close');
    }, 5000);
    form.trigger('reset');
    imei_1.focus();
    return;
  }

  // Check if either IMEI already exists in the container
  const alreadyExists = container.some((item) => item.includes(imei_1.val()) || item.includes(imei_2.val()));

  if (!alreadyExists) {
    // Create a new item with the IMEI numbers and add it to the container
    const newItem = [imei_1.val(), imei_2.val()];
    container.push(newItem);
    total.text(container.length);
    form.trigger('reset');
    imei_1.focus();
    waitRoom.find('.list-group').append(
      `<li class="list-group-item d-flex justify-content-between align-items-center">
        <span class="text-success fw-bold">IMEI 1: ${newItem.join(' <===> IMEI 2: ')}</span>
        <button class="btn btn-sm delete-item" data-index="${container.length - 1}">
          <span class="material-icons text-danger">delete</span>
        </button>
      </li>`
    );
  } else {
    const note = '<div class="alert alert-warning alert-dismissible fade show" role="alert">IMEI numbers already scanned or added in the list\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>';
    $(note).insertBefore(form);
    setTimeout(() => {
      $('.alert').alert('close');
    }, 5000);
    form.trigger('reset');
    imei_1.focus();
  }
});

// Handle delete button click
waitRoom.on('click', '.delete-item', function () {
  const index = $(this).data('index'); // Get the index of the item
  container.splice(index, 1); // Remove the item from the container
  total.text(container.length); // Update total count

  // Re-render the list with updated container
  const updatedList = container
    .map(
      (item, i) =>
        `<li class="list-group-item d-flex justify-content-between align-items-center">
           <span class="text-success fw-bold">IMEI 1: ${item.join(' <===> IMEI 2: ')}</span>
           <button class="btn btn-sm delete-item" data-index="${i}">
             <span class="material-icons text-danger">delete</span>
           </button>
         </li>`
    )
    .join('');
  waitRoom.find('.list-group').html(updatedList);
});

send.on('click', () => {
  if (container.length === 0) {
    const note = '<div class="alert alert-warning alert-dismissible fade show" role="alert">No Items Scanned!!! Please scan IMEI numbers\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>';
    $(note).insertBefore(form);
    setTimeout(() => {
      $('.alert').alert('close');
    }, 5000);
    imei_1.focus();
    return;
  }

  if (name.val().length === 0 || cost_price.val().length === 0 || supplier.val().length === 0) {
    const note = '<div class="alert alert-warning alert-dismissible fade show" role="alert">Please enter the phone name, cost price and Suppllier\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>';
    $(note).insertBefore(form);
    setTimeout(() => {
      $('.alert').alert('close');
    }, 5000);
    cost_price.focus();
    return;
  }

  $.ajax({
    url: '/system_core_1/add_to_stock/',
    type: 'POST',
    data: {
      data: JSON.stringify(container),
      name: name.val(),
      cost_price: cost_price.val(),
      category: category.val(),
      specs: specs.val(),
      supplier: supplier.val(),
    },
    beforeSend() {
      load.show();
    },
    success: (response) => {
      load.hide()
      if (response.status === 200) {
        container = [];
        waitRoom.find('.list-group').empty();
        form.trigger('reset');
        imei_1.focus();
        if (response.data.length > 0) {
          const note = '<div class="alert alert-danger alert-dismissible fade show" role="alert">Items Displayed already exist\
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
          </div>';
          $(note).insertBefore(form);
          setTimeout(() => {
            $('.alert').alert('close');
          }, 5000)
          response.data.forEach((item) => {
            waitRoom.find('.list-group').append(
              `<li class="list-group-item text-danger fw-bold">IMEI 1: ${item[0]} <===> IMEI 2: ${item[1]}</li>`,
            );
          });
        } else {
          const note = '<div class="alert alert-success alert-dismissible fade show" role="alert">Successfully added to stock\
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
                        </div>';
          $(note).insertBefore(form);
          setTimeout(() => {
            $('.alert').alert('close');
          }, 5000);
        }
      } else {
        const note = '<div class="alert alert-danger alert-dismissible fade show" role="alert">Failed to add to stock\
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
                    </div>';
        $(note).insertBefore(form);
        setTimeout(() => {
          $('.alert').alert('close');
        }, 5000);
      }
    },
    error: (error) => {
      const note = '<div class="alert alert-danger alert-dismissible fade show" role="alert">Failed to add to stock\
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
                </div>';
      $(note).insertBefore(form);
      setTimeout(() => {
        $('.alert').alert('close');
      }, 5000);
    },
  });
});

$(document).ready(() => {
  // Listen for input in the first IMEI field
  $('#id_device_imei').on('input', function () {
    // If the input length is equal to 15 characters
    if ($(this).val().length === 15) {
      // Focus on the second IMEI field
      $('#id_device_imei_2').focus();
    }
  });
});
