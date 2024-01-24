
function agent_stock_chart_details(url, dest, chartType, loader) {

    let allAgentsStocks = null;
    let allAgentCtx = null;
    let date = new Date();

    if (allAgentsStocks === null) {
        allAgentCtx = $(dest).get(0).getContext('2d');
    }

    function fetchAndUpdateDailyData() {
        let modelList = [];
        let total = [];
        let colors = [];
        let overallTotal = 0;
        
        $.ajax({
            url: url,
            method: "GET",
            contentType: "application/json",
            beforeSend: function () {
                const load = $(loader)
                load.addClass('loading-message');
            },
            success: function (data) {
                const load = $(loader)
                load.removeClass('loading-message');

                $.each(data, function (model, value) {
                    if (model !== "Total") {
                        modelList.push(model);
                        total.push(value);
                    }
                    overallTotal === 0 ? overallTotal = data["Total"] : overallTotal;
                    
                });

                for (let i = 0; i < modelList.length; i++) {
                    let num1 = Math.round(Math.random() * 255 + 1);
                    let num2 = Math.round(Math.random() * 255 + 1);
                    let num3 = Math.round(Math.random() * 255 + 1);
                    colors.push(`rgb(${num1}, ${num2}, ${num3})`);
                }
                
                if (allAgentsStocks === null) {
                    allAgentsStocks = new Chart(allAgentCtx, {
                        type: chartType,
                        data: {
                            labels: modelList,
                            datasets: [{
                                label: "Total " + `${overallTotal}`,
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
                                    text: 'Total overall stock ' + `${overallTotal}`,
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
                    allAgentsStocks.data.labels = labelsList;
                    allAgentsStocks.data.datasets[0].data = total;
                    allAgentsStocks.update();
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
const url_agents_stock = "/system_core_1/get_agents_stock_json/";
const dest_all_stock = '.all_agents_stock_chart';
const chartType = 'doughnut';
const loader_all_stock = '.loading-message-stock';

const url_main_stock = "/system_core_1/get_main_stock_analysis/";
const dest_main_stock = '.main_stock_chart';
const loader_main_stock = '.loading-message-shop';
const chartType_main_stock = 'doughnut';

agent_stock_chart_details(
    url_agents_stock, dest_all_stock,
    chartType, loader_all_stock);

agent_stock_chart_details(
    url_main_stock, dest_main_stock,
    chartType_main_stock, loader_main_stock);