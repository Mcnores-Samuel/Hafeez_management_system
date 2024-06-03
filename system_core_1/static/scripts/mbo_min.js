const mboPending = () => {
  $('document').ready(() => {
    const note = $('.pending-sales-notice');
    function getPendingUpdates() {
      $.ajax({
        url: '/system_core_1/get_total_pending_contracts/',
        method: 'GET',
        contentTpe: 'application/json',
        success(data) {
          if (data) {
            note.text(`${data.total_pending_contracts}`);
          }
        },
      });
    }
    getPendingUpdates();
    setInterval(getPendingUpdates, 5 * 60 * 1000);
  });
};

mboPending();

const mboApproved = () => {
  $('document').ready(() => {
    const note = $('.approved-sales-notice');
    function getApprovedUpdates() {
      $.ajax({
        url: '/system_core_1/get_total_approved_contracts/',
        method: 'GET',
        contentTpe: 'application/json',
        success(data) {
          if (data) {
            note.text(`${data.total_approved_contracts}`);
          }
        },
      });
    }
    getApprovedUpdates();
    setInterval(getApprovedUpdates, 5 * 60 * 1000);
  });
}

mboApproved();


const mboRejected = () => {
  $('document').ready(() => {
    const note = $('.rejected-sales-notice');
    function getRejectedSales() {
      $.ajax({
        url: '/system_core_1/get_total_rejected_contracts/',
        method: 'GET',
        contentTpe: 'application/json',
        success(data) {
          if (data) {
            note.text(`${data.total_rejected_contracts}`);
          }
        },
      });
    }
    getRejectedSales();
    setInterval(getRejectedSales, 5 * 60 * 1000);
  });
}

mboRejected();