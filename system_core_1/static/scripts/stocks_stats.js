let allAgentsStocks = null;
let allAgentCtx = null;

function inStockStats() {
    let allAgentsStocks = null;
    let allAgentCtx = $('.all_agents_stock_chart').get(0);

    function updateChart() {
        let labelsList = [];
        let dataList = [];

        $.ajax({
            url: "/system_core_1/get_agents_stock_json/",
            method: "GET",
            contentType: "application/json",
            beforeSend: function () {
                const load = $('.loading-message-stock');
                load.addClass('loading-message');
            },
            success: function (data) {
                const load = $('.loading-message-stock');
                load.removeClass('loading-message');

                Object.keys(data).forEach(function (key) {
                    if (key !== "Total") {
                        labelsList.push(key);
                        dataList.push(data[key]);
                    }
                });

                const layout = {
                    title: `${data.Total}` + ' In Stock',
                    margin: { t: 50, b: 50, l: 50, r: 50 },
                    plot_bgcolor: 'rgba(0,0,0,0)',
                    paper_bgcolor: 'rgba(0,0,0,0)'
                };

                if (allAgentsStocks === null) {
                    allAgentsStocks = Plotly.newPlot(allAgentCtx, [{
                        labels: labelsList,
                        values: dataList,
                        hole: .4,
                        type: 'pie',
                    }], layout, { responsive: true, displaylogo: false });
                } else {
                    Plotly.react(allAgentCtx, [{
                        labels: labelsList,
                        values: dataList,
                        hole: .4,
                        type: 'pie',
                    }], layout, { responsive: true, displaylogo: false });
                }
                setTimeout(updateChart, 5 * 60 * 1000);
            },
            error: function (err) {
                console.log(err);
            }
        });
    }
    updateChart();
}

inStockStats();