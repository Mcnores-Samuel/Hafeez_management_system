import { metricsRender } from './metric_render.js';

$(document).ready(function() {
    const metricsBtn = $('#metrics');
    const container = $('#container');
    const pagination = $('#pagination');
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
                metricsCharts(response.data);
                loader.hide();
            },
            error: function(response) {
                container.html(response.responseText);
            }
        });
    }

    metricsBtn.click(function() {
        container.empty();
        pagination.empty();
        metricsRender(container);
        getData();
    });
});
