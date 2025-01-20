import metricsRender from './metric_render.js';
import { dailyMetricsChart, availableStock,
    dailyPaymentsChart, stockByIndividuals,
    overdueStock, airtelMonthlySalesChart } from './airtel_metric_charts.js';

$(document).ready(function() {
    const metricsBtn = $('#metrics');
    const container = $('#container');
    const pagination = $('.pagination');
    const loader = $('#loader');

    function getData() {
        $.ajax({
            url: '/system_core_1/metrics/',
            type: 'GET',
            contentType: 'application/json',
            beforeSend() {
                loader.show();
            },
            success: function(response) {
                dailyMetricsChart(response.data);
                availableStock(response.data);
                airtelMonthlySalesChart(response.data);
                dailyPaymentsChart(response.data);
                stockByIndividuals(response.data);
                overdueStock(response.data);
                loader.hide();
            },
            error: function(response) {
                container.html(response.responseText);
            }
        });
    }

    if (metricsBtn.length) {
        metricsBtn.on('click', function() {
            metricsRender();
            getData();
            container.show();
            pagination.hide();
        });
    } else {
        metricsRender();
        getData();
        container.show();
        pagination.hide();
    }
});
