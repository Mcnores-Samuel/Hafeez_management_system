$(document).ready(function() {
    const partner = $('#partnerID')
    const loader = $('#loader').hide()

    partner.on('change', function() {
        const partner_id = partner.val()
        $.ajax({
            url: '/system_core_1/data_per_partner/',
            type: 'POST',
            data: {
                partner: partner_id
            },
            beforeSend() {
                loader.show()
            },
            success: function(response) {
                loader.hide()
                invoiceTable(response.invoices)
            }
        })
    }
    )
});

const dateFormat = (time) => {
    const date = new Date(time)
    return date.toDateString()
}


const formatValue = (value) => {
    return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

const invoiceTable = (data) => {
    const container = $('.container')
    $('#tableBody').empty()
    $('.modal').remove()
    data.forEach(element => {
        $('#tableBody').append(
            `<tr>
                <td><button type="button" class="btn btn-secondary btn-sm" data-bs-toggle="modal" data-bs-target="#${element.invoice_number.replace(/\W/g, "_")}">${element.invoice_number}</button></td>
                <td>${dateFormat(element.invoice_date)}</td>
                <td>${element.total_invoice_items}</td>
                <td>MK${formatValue(element.original_cost)}</td>
                <td>MK${formatValue(element.cost_per_ex_rate)}</td>
                <td>${element.total_items_sold}</td>
                <td>MK${formatValue(element.total_amount_paid)}</td>
                <td>MK${formatValue(element.last_payment_amount)}</td>
                <td>${dateFormat(element.last_payment_date)}</td>
                <td>${element.is_paid ? 'unpaid' : 'paid'}</td>
            </tr>`
        )
        let modal = $(
            `<div class="modal fade" id="${element.invoice_number.replace(/\W/g, "_")}" tabindex="-1" aria-labelledby="${element.invoice_number}ModalLabel" aria-hidden="undefined">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                    <div class="modal-header">
                        <h5>Table List of Items on Invoice ${element.invoice_number}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="table-container">
                        <table class="table" id="invoiceTable">
                            <thead>
                                <tr>
                                    <th>Item Name</th>
                                    <th>IMEI Number</th>
                                    <th>Original Cost</th>
                                    <th>Cost by rate</th>
                                    <th>Date collected</th>
                                    <th>Sold</th>
                                    <th>Price Sold</th>
                                    <th>Payment Status</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody id="invoiceItems-${element.invoice_number.replace(/\W/g, "_")}">

                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            `
        )

        container.append(modal)

        element.items.forEach(item => {
            $(`#invoiceItems-${element.invoice_number.replace(/\W/g, "_")}`).append(
                `<tr style="background-color: ${item.sold ? 'rgba(221, 118, 118, 0.2)' : 'rgba(130, 192, 130, 0.2)'}">
                    <td>${item.name}</td>
                    <td>${item.device_imei}</td>
                    <td>MK${formatValue(item.cost)}</td>
                    <td>MK${formatValue(item.cost_per_ex_rate)}</td>
                    <td>${dateFormat(item.collected_on)}</td>
                    <td>${item.sold ? 'yes' : 'no'}</td>
                    <td>MK${formatValue(item.price)}</td>
                    <td>${item.pending ? 'pending' : 'freezed state'}</td>
                    <td>${item.in_stock ? 'in stock' : 'out of stock'}</td>
                </tr>`
            )
        })
    });
}
