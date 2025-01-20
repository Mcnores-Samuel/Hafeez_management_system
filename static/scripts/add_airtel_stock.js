let container = [];
const form = $('form');
const imei_1 = $('#id_device_imei');
const device_type = $('#id_device_type');
const waitRoom = $('#waiting-room');
const send = $('#submit');
const total = $('#total').text(container.length);

imei_1.on('change', (e) => {
  e.preventDefault();

  if (imei_1.val().length !== 15) {
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
  const alreadyExists = container.some((item) => item.includes(imei_1.val()));

  if (!alreadyExists) {
    // Create a new item with the IMEI numbers and add it to the container
    container.push(imei_1.val());
    waitRoom.find('.list-group').append(
      `<li class="list-group-item text-success fw-bold">IMEI 1: ${imei_1.val()}</li>`,
    );
    total.text(container.length);
    form.trigger('reset');
    imei_1.focus();
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

  if (device_type.val() === '') {
    const note = '<div class="alert alert-warning alert-dismissible fade show" role="alert">Please select the type of the scanned devices\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>';
    $(note).insertBefore(form);
    setTimeout(() => {
      $('.alert').alert('close');
    }, 5000);
    cost_price.focus();
    return;
  }

  const load = $('.loading-target');
  load.addClass('loading-message');

  $.ajax({
    url: '/system_core_1/add_airtel_devices_stock/',
    type: 'POST',
    data: {
      data: JSON.stringify(container),
      device_type: device_type.val(),
    },
    success: (response) => {
      load.removeClass('loading-message');
      if (response.status === 200) {
        container = [];
        total.text(container.length);
        waitRoom.find('.list-group').empty();
        form.trigger('reset');
        imei_1.focus();
        if (response.data.length > 0) {
          const note = '<div class="alert alert-danger alert-dismissible fade show" role="alert">IMEI numbers already scanned or added in the list\
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
          </div>';
          $(note).insertBefore(form);
          setTimeout(() => {
            $('.alert').alert('close');
          }, 5000);
          response.data.forEach((item) => {
            waitRoom.find('.list-group').append(
              `<li class="list-group-item text-danger fw-bold">IMEI 1: ${item}</li>`,
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
        const note = '<div class="alert alert-danger alert-dismissible fade show" role="alert">Failed to add to stock something went wrong\
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
      load.removeClass('loading-message');
      setTimeout(() => {
        $('.alert').alert('close');
      }, 5000);
    },
  });
});