const callModal = () => {
  const allowWebBtn = $('#webpush-subscribe-button');
  const modal = $('#web_push_request');

  if (allowWebBtn.text().includes('Subscribe')) {
    modal.modal('show');
  } else {
    modal.modal('hide');
  }
};

$(document).ready(() => {
  setTimeout(callModal, 30000);
});
