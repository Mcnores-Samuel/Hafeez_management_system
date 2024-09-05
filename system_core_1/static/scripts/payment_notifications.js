$(document).ready(function() {
    const noteBadge = $('.note_badge');
    const offcanvasBody = $('.offcanvas-body');

    // Function to fetch and display payment notifications
    function fetchPaymentNotifications() {
        $.ajax({
            url: '/system_core_1/paymentsNotification/',
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                noteBadge.text(response.total_payments);
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
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        };
        return date.toLocaleString(undefined, options);
    }

    // Function to render payment notifications
    function renderPaymentNotifications(data) {
        offcanvasBody.empty();
        data.forEach(function(item) {
            const notification = `
                <a class="card mb-3 shadow-sm border-0 rounded-lg" href="/system_core_1/paymentsNotification/${item.id}" style="text-decoration: none;">
                    <div class="card-body bg-light rounded-lg">
                        <div class="d-flex justify-content-between mb-2">
                            <h5 class="card-title fw-bold text-primary mb-0">${item.promoter}</h5>
                        </div>
                         <span class="badge bg-success">${formatTimestamp(item.payment_date)}</span>
                        <p class="card-text mb-1">
                            <strong class="text-info">Amount:</strong> $${item.amount.toLocaleString()}
                        </p>
                        <p class="card-text mb-1">
                            <strong class="text-info">MIFI Paid:</strong> ${item.total_mifi.toLocaleString()}
                        </p>
                        <p class="card-text mb-1">
                            <strong class="text-info">IDU Paid:</strong> ${item.total_idu.toLocaleString()}
                        </p>
                    </div>
                </a>
            `;
            offcanvasBody.append(notification);
        });
    }

    fetchPaymentNotifications();

    setInterval(function() {
        fetchPaymentNotifications();
    }, 60000);
});