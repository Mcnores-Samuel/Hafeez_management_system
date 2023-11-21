let allAgentsStocks = null;
let allAgentCtx = null;

function inStockStats() {
    if (allAgentsStocks === null) {
        allAgentCtx = $('.all_agents_stock_chart').get(0).getContext('2d');
    }

    let chartType = "doughnut";

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
                }
                );

                if (allAgentsStocks === null) {
                    allAgentsStocks = new Chart(allAgentCtx, {
                        type: chartType,
                        data: {
                            labels: labelsList,
                            datasets: [{
                                label: 'In Stock',
                                data: dataList,
                                backgroundColor: ['#0B666A', '#97FEED', '#2B2A4C',
                                '#FF9B42', '#FFD56F', '#411020', '#FFCA3A', '#E11299',
                                '#060047', '#4D455D', '#1A4D2E', '#3AB0FF', '#38928f',
                                '#fffffb', '#264720', '#217799'
                                ]
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            legend: {
                                display: false
                            },
                            title: {
                                display: true,
                                text: 'Stocks'
                            },
                            animation: {
                                animateScale: true,
                                animateRotate: true
                            },
                            maintainAspectRatio: false,
                            scales: {
                                yAxes: [{
                                    ticks: {
                                        beginAtZero: true,
                                        stepSize: 1
                                    }
                                }]
                            },
                            barPercentage: 0.7,
                            categoryPercentage: 0.7,
                            plugins: {
                                title: {
                                    display: true,
                                    text: `${data.Total}` + ' In Stock',
                                    color: 'navy',
                                    position: 'bottom',
                                    font: {
                                        weight: 'bold'
                                    },
                                    padding: 8,
                                    fullSize: true,
                                }
                            }

                        }
                    });

                } else {
                    allAgentsStocks.data.labels = labelsList;
                    allAgentsStocks.data.datasets[0].data = dataList;
                    allAgentsStocks.update();
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
