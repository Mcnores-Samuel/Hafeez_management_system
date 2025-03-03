import { formatValue } from './formatValue.js';

$(document).ready(function () {
    const loader = $('#availableStockcostLoader');
    const cost = $('#availableStockCost');
    
    function fetchData() {
        $.ajax({
        url: '/system_core_1/availableStockCost/',
        method: 'GET',
        contentType: 'application/json',
        beforeSend() {
            loader.show();
        },
        success(data) {
            loader.hide();
            console.log(data);
            availableStockCost(data);
        },
        });
    }
    fetchData();

    function availableStockCost(data) {
        cost.html(`MK${formatValue(data.total_cost)}`);
    }
});