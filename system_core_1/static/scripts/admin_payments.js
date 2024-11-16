$(document).ready(function() {
    const container = $('#container');
    const loader = $('#loader');
    const currPaymentsBtn = $('#currentPayments');
    const concludedPaymentsBtn = $('#concludedPayments');
    const pagination = $('#pagination');
    const row_container = $(`<div class="row"></div>`);

    function fetchPaymentNotifications(url, concluded) {
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            beforeSend() {
                loader.show();
            },
            success: function(response) {
                loader.hide();
                if (concluded === false) {
                    renderCurrentPayments(response.data);
                } else {
                    renderConcludedPayments(response.data);
                }
            },
            error: function(xhr, status, error) {
                console.error("Error fetching data: ", error);
            }
        });
    }

    // Function to format a timestamp
    function formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        const options = {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        };
        return date.toLocaleString(undefined, options);
    }

    // Function to render payment notifications
    function renderCurrentPayments(data) {
        data.forEach(function(item) {
            const notification = `
                <div class="col-md-4 col-sm-6 mb-4">
                    <div class="card shadow-sm round rounded-lg" style="text-decoration: none;">
                        <div class="card-header bg-primary text-white text-center">
                            <h5 class="card-title fw-bold mb-0">${item.promoter}</h5>
                        </div>
                        <div class="card-body bg-light rounded-lg">
                            <span class="badge bg-success">${formatTimestamp(item.payment_date)}</span>
                            <p class="card-text mb-1">
                                <strong class="text-info">Amount:</strong> $${item.amount_paid.toLocaleString()}
                            </p>
                            <p class="card-text mb-1">
                                <strong class="text-info">Payment Type:</strong> <span>${item.payment_method}</span>
                            <p class="card-text mb-1">
                                <strong class="text-info">MIFI Paid:</strong> <span>${item.total_mifi_paid.toLocaleString()}</span>
                            </p>
                            <p class="card-text mb-1">
                                <strong class="text-info">IDU Paid:</strong> <span>${item.total_idu_paid.toLocaleString()}</span>
                            </p>
                            <p class="card-text mb-1">
                                <strong class="text-info">Total Paid:</strong> <span>${item.total_devices_paid.toLocaleString()}</span>
                            </p>
                            <p class="card-text mb-1">
                                <strong class="text-info">Issued By:</strong> <span>${item.updated_by}</span>
                            </p>
                            <p class="card-text mb-1">
                                <strong class="text-info">Attended:</strong> <span>${item.seen ? "Yes" : "No"}</span>
                            </p>
                            <p class="card-text mb-1">
                                <strong class="text-info">validity:</strong> <span>${item.validity ? "valid" : "invalid"}</span>
                            </p>
                            <br>
                            <form action="/system_core_1/renewPayment/" method="post">
                                <input type="hidden" name="payment_id" value="${item.id}">
                                <button type="submit" class="btn common-bg btn-sm w-100 fw-bold">Renew</button>
                            </form>
                            <br>
                            <button class="btn btn-danger btn-sm w-100 fw-bold" data-bs-toggle="modal" data-bs-target="#Data${item.id}">delete</button>

                            <div class="modal fade" id="Data${item.id}" tabindex="-1" aria-labelledby="Data${item.id}View" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title text-center fw-bold">Delete Payment</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body common-bg">
                                            <form action="/system_core_1/deletePayment/" method="post" class="deleteForm">
                                                <input type="hidden" name="payment_id" value="${item.id}">
                                                <p class="text-danger fw-bold text-center">This action is irreversible, are you sure you want to delete this payment?</p>
                                                <button type="submit" class="btn btn-danger btn-sm w-100 deleteBtn">delete</button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>    
                        </div>
                    </div>
                </div>
            `;
            row_container.append(notification);
        });
        container.append(row_container);
    }

    function renderConcludedPayments(data) {
        data.forEach(function(item) {
            const notification = `
                <div class="col-md-4 col-sm-6 mb-4">
                    <div class="card shadow-sm round rounded-lg" style="text-decoration: none;">
                        <div class="card-header bg-primary text-white text-center">
                            <h5 class="card-title fw-bold mb-0">${item.promoter}</h5>
                        </div>
                        <div class="card-body common-bg rounded-lg">
                            <span class="badge bg-success">${formatTimestamp(item.payment_date)}</span>
                            <p class="card-text mb-1">
                                <strong class="text-info">Amount:</strong> $${item.amount_paid.toLocaleString()}
                            </p>
                            <p class="card-text mb-1">
                                <strong class="text-info">Payment Type:</strong> <span>${item.payment_method}</span>
                            <p class="card-text mb-1">
                                <strong class="text-info">MIFI Paid:</strong> <span>${item.total_mifi_paid.toLocaleString()}</span>
                            </p>
                            <p class="card-text mb-1">
                                <strong class="text-info">IDU Paid:</strong> <span>${item.total_idu_paid.toLocaleString()}</span>
                            </p>
                            <p class="card-text mb-1">
                                <strong class="text-info">Total Paid:</strong> <span>${item.total_devices_paid.toLocaleString()}</span>
                            </p>
                            <p class="card-text mb-1">
                                <strong class="text-info">Issued By:</strong> <span>${item.updated_by}</span>
                            </p>
                            <p class="card-text mb-1">
                                <strong class="text-info">Attended:</strong> <span>${item.seen ? "Yes" : "No"}</span>
                            </p>
                            <p class="card-text mb-1">
                                <strong class="text-info">validity:</strong> <span>${item.validity ? "valid" : "invalid"}</span>
                            </p>    
                        </div>
                    </div>
                </div>
            `;
            row_container.append(notification);
        });
        container.append(row_container);
    }

    currPaymentsBtn.on('click', function() {
        row_container.empty();
        container.empty();
        pagination.empty();
        loader.show();
        const url = '/system_core_1/currentPayments/';
        fetchPaymentNotifications(url, false);
    });

    concludedPaymentsBtn.on('click', function() {
        row_container.empty();
        container.empty();
        pagination.empty();
        loader.show();
        const url = '/system_core_1/concludedPayments/';
        fetchPaymentNotifications(url, true);
    });
});