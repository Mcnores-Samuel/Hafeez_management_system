let container = [];
const scannedItem = $('#data');
const form = $('#inputForm');
const waitingRoom = $('#waiting-room ul');
const deploy = $('#deploy');
const total = $('#total');
const csrf = $('#token');
const load = $('#loader');
total.text(container.length);
load.hide();

function updateWaitingRoom() {
  waitingRoom.html(
    container
      .map(
        (item, index) =>
          `<li class="list-group-item d-flex justify-content-between align-items-center">
             ${item} 
             <button class="btn btn-sm delete-item" data-index="${index}">
              <span class="material-icons text-danger">delete</span>
             </button>
           </li>`
      )
      .join('')
  );
  total.text(container.length);
}


function deployData() {
  form.on('submit', (e) => {
    e.preventDefault();
    if (scannedItem.val() === '') {
      return;
    }
    if (!container.includes(scannedItem.val().trim())) {
      container.push(scannedItem.val().trim());
      updateWaitingRoom();
      scannedItem.val('').focus();
    } else {
      const note = `<div class="alert alert-danger alert-dismissible fade show" role="alert">Item ${scannedItem.val()} already scanned\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>`;
      $(note).insertBefore(scannedItem);
      setInterval(() => {
        $('.alert').alert('close');
      }, 5000);
    }
    scannedItem.val('').focus();
  });

  waitingRoom.on('click', '.delete-item', function () {
    const index = $(this).data('index'); // Get index
    container.splice(index, 1); // Remove item
    updateWaitingRoom(); // Re-render the list
  });

  deploy.on('click', () => {
    if (container.length === 0) {
      const note = '<div class="alert alert-danger alert-dismissible fade show" role="alert">No items to deploy\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>';
      $(note).insertBefore(form);
      setInterval(() => {
        $('.alert').alert('close');
      }, 5000);
      return;
    }
    $.ajax({
      url: '/system_core_1/stock_taking/',
      type: 'POST',
      data: {
        csrfmiddlewaretoken: csrf.val(),
        data: JSON.stringify(container),
      },
      beforeSend() {
        load.show();
      },
      success(response) {
        if (response.status === 200) {
          load.hide();
          container = [];
          waitingRoom.html('');
          total.text(container.length);
          scannedItem.val('').focus();
          if (response.not_in_stock.length > 0) {
            waitingRoom.html(`<li class="list-group-item bg-danger">${response.not_in_stock.join('</li><li class="list-group-item bg-danger">')}</li>`);
            total.text(response.not_in_stock.length);
            const note = '<div class="alert alert-warning alert-dismissible fade show" role="alert">The following items are not in stock\
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
            </div>';
            $(note).insertBefore(form);
            setInterval(() => {
              $('.alert').alert('close');
            }, 5000);
          } else {
            const note = '<div class="alert alert-success alert-dismissible fade show" role="alert">Items deployed successfully\
              <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
              </div>';
            $(note).insertBefore(form);
            setInterval(() => {
              $('.alert').alert('close');
            }, 5000);
          }
        } else {
          const note = '<div class="alert alert-danger alert-dismissible fade show" role="alert">Error deploying items\
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
            </div>';
          $(note).insertBefore(form);
          setInterval(() => {
            $('.alert').alert('close');
          }, 5000);
        }
      },
      error() {
        const note = '<div class="alert alert-danger alert-dismissible fade show" role="alert">Error deploying items\
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
            </div>';
        $(note).insertBefore(form);
        setInterval(() => {
          $('.alert').alert('close');
        }, 5000);
      },
    });
  });
}
deployData();
