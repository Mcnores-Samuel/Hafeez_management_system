function yearly_sales_analysis(url, dest, chartType, loader) {
    let sales_analystChart = null;
    let yearly_analysisctx = null;

    if (sales_analystChart === null) {
        yearly_analysisctx = $(dest).get(0).getContext('2d');
    }

    let date = new Date();

    function fetchAndUpdateDailyData() {
        let modelList = [];
        let total = [];
        
        $.ajax({
            url: url,
            method: "GET",
            contentType: "application/json",
            beforeSend: function () {
                const load = $(loader);
                load.addClass('loading-message');
            },
            success: function (data) {
                const load = $(loader);
                load.removeClass('loading-message');

                $.each(data, function (key, value) {
                    modelList.push(key);
                    total.push(value);
                });
                
                if (sales_analystChart === null) {
                    sales_analystChart = new Chart(yearly_analysisctx, {
                        type: chartType,
                        data: {
                            labels: modelList,
                            datasets: [{
                                label: date.toDateString(),
                                data: total,
                                backgroundColor: ["#23435c"],
                                borderColor: ["#23435c"],
                                borderWidth: 2
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            events: ["mousemove"],
                            interaction: {
                                mode: "nearest",
                            },
                            plugins: {
                                title: {
                                    display: true,
                                    text: 'Daily Sales Analysis',
                                    color: 'navy',
                                    position: 'bottom',
                                    align: 'center',
                                    font: {
                                        weight: 'bold'
                                    },
                                    padding: 8,
                                    fullSize: true,
                                }
                            },
                            scales: {
                                x: {
                                    grid: {
                                        display: false,
                                        drawBorder: false,
                                    },
                                    ticks: {
                                        color: "navy",
                                        font: {
                                            weight: 'bold'
                                        },
                                    },
                                },
                                y: {
                                    grid: {
                                        display: false,
                                        drawBorder: false,
                                    },
                                    ticks: {
                                        color: "navy",
                                        font: {
                                            weight: 'bold'
                                        },
                                    },
                                },
                            },
 
                        }
                    });
                } else {
                    sales_analystChart.data.labels = labelsList;
                    sales_analystChart.data.datasets[0].data = total;
                    sales_analystChart.update();
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

const url_yearly = "/system_core_1/get_yearly_sales/"
const dest_yearly = ".yearly_sales_chart";
const chartType_yearly = "bar";
const loader_yearly = ".yearly_sales_chart_loader";
yearly_sales_analysis(url_yearly, dest_yearly, chartType_yearly, loader_yearly);