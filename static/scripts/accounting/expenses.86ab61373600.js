import { formatValue } from './formatValue.js';

$(document).ready(function () {
    const loader = $('#expenseLoader');
    const expense = $('#totalExpense');

    function fetchData() {
        $.ajax({
            url: '/system_core_1/get_total_expenses/',
            method: 'GET',
            contentType: 'application/json',
            beforeSend() {
                loader.show();
            },
            success(data) {
                loader.hide();
                console.log(data);
                totalExpense(data);
            },
        });
    }
    fetchData();

    function totalExpense(data) {
        expense.html(`MK${formatValue(data.total_expenses)}`);
    }
});