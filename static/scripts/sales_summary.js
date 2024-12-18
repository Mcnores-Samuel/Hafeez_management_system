import { dailySalesChart, monthlySalesChart, stockChart } from './sales_summary_charts.js';
import { renderTable, stockTable } from './data_output_summary.js';

$(document).ready(function() {
    const agentFilter = $('#id_user');
    const dateFilter = $('#id_date');
    const monthFilter = $('#id_month');
    const yearFilter = $('#id_year');
    const loader = $('#loader');
    const username = $('.id_name');
    loader.hide();

    function fetchSalesSummaryData() {
        $.ajax({
            url: '/system_core_1/sales_stock_summry',
            type: 'GET',
            data: {
                agent: agentFilter.val(),
                date: dateFilter.val(),
                month: monthFilter.val(),
                year: yearFilter.val()
            },
            dataType: 'json',
            beforeSend() {
                loader.show();
                $('#sales_table_body').empty();
                $('#stock_table_body').empty();
                $('#stock_table_container').empty();
            },
            success: function(response) {
                loader.hide();
                username.text(response.data.username);
                dailySalesChart(response.data.daily_sales, dateFilter.val());
                monthlySalesChart(response.data.monthly_sales, yearFilter.val(), monthFilter.val());
                stockChart(response.data.stock);
                renderTable(response.data.monthly_sales, $('#sales_table_body'));
                renderTable(response.data.stock, $('#stock_table_body'));
                stockTable(response.data.stock_details, $('#stock_table_container'));
            },
            error: function(xhr, status, error) {
                console.error("Error fetching data: ", error);
            }
        });
    }


    agentFilter.change(function() {
        loader.show();
        fetchSalesSummaryData();
    });

    dateFilter.change(function() {
        loader.show();
        fetchSalesSummaryData();
    });

    monthFilter.change(function() {
        loader.show();
        fetchSalesSummaryData();
    });

    yearFilter.change(function() {
        loader.show();
        fetchSalesSummaryData();
    });
});