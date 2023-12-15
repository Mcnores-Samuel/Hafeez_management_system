let main_stockChart = null;
let main_stockctx = null;


function main_stock_chart_details() {

    if (main_stockChart === null) {
        main_stockctx = $('.main_stock_detailed_analysis').get(0).getContext('2d');
    }

    let date = new Date();
    let chartType = "bar";

    function fetchAndUpdateDailyData() {
        let modelList = [];
        let total = [];
        
        $.ajax({
            url: "/system_core_1/get_source_stock/",
            method: "GET",
            contentType: "application/json",
            beforeSend: function () {
                const load = $('.loading-message-main-stock')
                load.addClass('loading-message');
            },
            success: function (data) {
                const load = $('.loading-message-main-stock')
                load.removeClass('loading-message');

                modelList = data.map(item => item[0])
                total = data.map(item => item[1])
                
                if (main_stockChart === null) {
                    main_stockChart = new Chart(main_stockctx, {
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
                    main_stockChart.data.labels = labelsList;
                    main_stockChart.data.datasets[0].data = nums;
                    main_stockChart.update();
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
main_stock_chart_details();