$(document).ready(function() {
    const container = $('#container');
    const loader = $('#loader');
    const currPaymentsBtn = $('#currentPayments');
    const pagination = $('#pagination');
    const row_container = $(`<div class="row"></div>`);

    function fetchPaymentNotifications() {
        $.ajax({
            url: '/system_core_1/currentPayments/',
            type: 'GET',
            dataType: 'json',
            beforeSend() {
                loader.show();
            },
            success: function(response) {
                loader.hide();
                renderPaymentNotifications(response.data);
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
    function renderPaymentNotifications(data) {
        data.forEach(function(item) {
            const notification = `
                <div class="col-md-4 col-sm-6 mb-4">
                    <div class="card shadow-sm round rounded-lg" style="text-decoration: none;">
                        <div class="card-body bg-light rounded-lg">
                            <div class="d-flex justify-content-between">
                                <h5 class="card-title fw-bold text-primary mb-0 text-center">${item.promoter}</h5>
                            </div>
                            <span class="badge bg-success">${formatTimestamp(item.payment_date)}</span>
                            <p class="card-text mb-1">
                                <strong class="text-info">Amount:</strong> $${item.amount_paid.toLocaleString()}
                            </p>
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
                        </div>
                    </div>
                </div>
            `;
            row_container.append(notification);
            container.append(row_container);
        });
    }


    currPaymentsBtn.on('click', function() {
        container.empty();
        pagination.empty();
        fetchPaymentNotifications();
    });

});