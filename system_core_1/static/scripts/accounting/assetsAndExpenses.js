import { formatValue } from './formatValue.js';

$(document).ready(function () {
    
    function fetchData(url, loader, dest) {
        $.ajax({
        url: url,
        method: 'GET',
        contentType: 'application/json',
        beforeSend() {
            loader.show();
        },
        success(data) {
            loader.hide();
            let total = Object.values(data)[0];
            dest.html(`MK${formatValue(total)}`);
        },
        });
    }

    const loader = $('#availableStockcostLoader');
    const costDest1 = $('#availableStockCost');
    const url1 = '/system_core_1/availableStockCost/';
    fetchData(url1, loader, costDest1);

    const loader2 = $('#expenseLoader');
    const expense = $('#totalExpense');
    const url2 = '/system_core_1/get_total_expenses/';
    fetchData(url2, loader2, expense);

    const networthLoader = $('#networthLoader');
    const networth = $('#networth');
    const url3 = '/system_core_1/networth/';
    fetchData(url3, networthLoader, networth);

    const loader4 = $('#totalAssetsLoader');
    const totalAssets = $('#totalAssets');
    const url4 = '/system_core_1/total_assets/';
    fetchData(url4, loader4, totalAssets);

    const loader5 = $('#totalLiabilitiesLoader');
    const totalLiabilities = $('#totalLiabilities');
    const url5 = '/system_core_1/total_liabilities/';
    fetchData(url5, loader5, totalLiabilities);
});