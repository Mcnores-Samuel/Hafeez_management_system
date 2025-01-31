$(document).ready(function() {
    const exRateForm = $('#ex_rate_form')
    const loader = $('#loader').hide()
    const exRateInput = $('#current_ex_rate')
    

    exRateForm.on('submit', function(e) {
        e.preventDefault()
        const exRate = exRateInput.val()
        if (exRate === '') {
            $('#notification').text('Please enter a value, the field cannot be empty')
            return
        }
        $.ajax({
            url: '/system_core_1/add_exchange_rate/',
            type: 'POST',
            data: {
                current_ex_rate: exRate
            },
            beforeSend() {
                loader.show()
            },
            success: function(response) {
                loader.hide()
                exRateInput.val('')
                $('#ex_rate_view').text(response.current_ex_rate)
            }
        })
    })

    const getExRate = () => {

        const fetchExRate = () => {
            $.ajax({
                url: '/system_core_1/get_exchange_rate/',
                type: 'GET',
                success: function(response) {
                    $('#ex_rate_view').empty()
                    $('#ex_rate_view').text(response.current_ex_rate)
                }
            })
        }
        fetchExRate()
        setInterval(fetchExRate, 5000 * 60) // 5 minutes
    }

    getExRate()


    const getOutstandingInvoices = () => {
        const getInvoices = () => {
            $.ajax({
                url: '/system_core_1/get_outstanding_invoice/',
                type: 'GET',
                success: function(response) {
                    $('#outstanding_invoices').empty()
                    $('#outstanding_invoices').text(response.total_outstanding)
                }
            })
        }
        getInvoices()
        setInterval(getInvoices, 5000 * 60) // 5 minutes
    }

    getOutstandingInvoices()
});