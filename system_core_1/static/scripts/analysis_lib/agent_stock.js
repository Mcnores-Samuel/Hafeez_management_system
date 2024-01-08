let agent_stockChart = null;
let agent_stockctx = null;


function agent_stock_chart_details() {

    if (agent_stockChart === null) {
        agent_stockctx = $('.StockChart').get(0).getContext('2d');
    }

    let date = new Date();
    let chartType = "doughnut";

    function fetchAndUpdateDailyData() {
        let modelList = [];
        let total = [];
        let colors = [];
        
        $.ajax({
            url: "/system_core_1/get_individual_agent_stock/",
            method: "GET",
            contentType: "application/json",
            beforeSend: function () {
                const load = $('.loading-message-agent-stock')
                load.addClass('loading-message');
            },
            success: function (data) {
                const load = $('.loading-message-agent-stock')
                load.removeClass('loading-message');

                $.each(data, function (model, value) {
                    modelList.push(model);
                    total.push(value);
                });

                for (let i = 0; i < modelList.length; i++) {
                    let num1 = Math.round(Math.random() * 255 + 1);
                    let num2 = Math.round(Math.random() * 255 + 1);
                    let num3 = Math.round(Math.random() * 255 + 1);
                    colors.push(`rgb(${num1}, ${num2}, ${num3})`);
                }
                
                if (agent_stockChart === null) {
                    agent_stockChart = new Chart(agent_stockctx, {
                        type: chartType,
                        data: {
                            labels: modelList,
                            datasets: [{
                                label: date.toDateString(),
                                data: total,
                                backgroundColor: colors,
                                borderColor: colors,
                                borderWidth: 2
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            animation: {
                                animateScale: true,
                                animateRotate: true
                            },
                            events: ["mousemove"],
                            interaction: {
                                mode: "nearest",
                            },
                            plugins: {
                                title: {
                                    display: true,
                                    text: 'Stock Analysis',
                                    color: 'navy',
                                    position: 'bottom',
                                    align: 'center',
                                    font: {
                                        weight: 'bold'
                                    },
                                    padding: 8,
                                    fullSize: true,
                                },
                                legend: {
                                    display: true,
                                    position: 'right',
                                    labels: {
                                        color: 'black',
                                        font: {
                                            size: 10,
                                            weight: 'bold'
                                        }
                                    }
                                },
                            },
                        }
                    });
                } else {
                    agent_stockChart.data.labels = labelsList;
                    agent_stockChart.data.datasets[0].data = total;
                    agent_stockChart.update();
                }
                setTimeout(fetchAndUpdateDailyData, 5 * 60 * 1000);
            },
            error: function (err) {
                console.error(err);
            }
        });
    }
    fetchAndUpdateDailyData();
}
agent_stock_chart_details();