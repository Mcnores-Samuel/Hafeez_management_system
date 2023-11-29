const months = [
    "January", "February", 
    "March", "April", "May", 
    "June", "July", "August",
    "September", "October", 
    "November", "December"
];


let weeklySalesChart = null;
let weeklyCtx = null;

let salesByAgentChart = null;
let salesByAgentCtx = null;

let dailyCtx = null;
let dailySalesChart = null;

/**
 * Update the monthly sales chart
 * @returns {void}
 * @async - This function is asynchronous
 * @function updateMonthlyChart - Update the monthly sales chart
 * @memberof module:system_core_1/static/scripts/data_charts.js
 * @inner - updateMonthlyChart
 * @param {void} - This function does not take any parameters
 * @example - updateMonthlyChart();
 * updateMonthlyChart();
 * @requires jQuery from jquery
 * @requires Chart  from chart.js
 */
function updateDailyChart() {

    if (dailySalesChart === null) {
        dailyCtx = $('.daily_sales_chart').get(0).getContext('2d');
    }

    let date = new Date();
    let chartType = "line";

    function fetchAndUpdateDailyData() {
        let modelList = [];
        let total = [];
        
        $.ajax({
            url: "/system_core_1/get_daily_sales_json/",
            method: "GET",
            contentType: "application/json",
            beforeSend: function () {
                const load = $('.loading-message-daily')
                load.addClass('loading-message');
            },
            success: function (data) {
                const load = $('.loading-message-daily')
                load.removeClass('loading-message');

                $.each(data, function (model, value) {
                    modelList.push(model);
                    total.push(value);
                });

                if (dailySalesChart === null) {
                    dailySalesChart = new Chart(dailyCtx, {
                        type: chartType,
                        data: {
                            labels: modelList,
                            datasets: [{
                                label: date.toDateString(),
                                data: total,
                                backgroundColor: ["#877B89", "blue", "green", "yellow", "gray"],
                                borderColor: ["#877B89", "blue", "green", "yellow", "gray"],
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
                            }
                        }
                    });
                } else {
                    dailySalesChart.data.labels = labelsList;
                    dailySalesChart.data.datasets[0].data = nums;
                    dailySalesChart.update();
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
updateDailyChart();


function updateWeeklyChart() {
    if (weeklySalesChart === null) {
        weeklyCtx = $('.Weekly_sales_chart').get(0).getContext('2d');
    }
    
    let labelsList = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    let chartType = "line";

    function fetchAndUpdateWeeklyData() {
        let nums = [];

        $.ajax({
            url: "/system_core_1/get_weekly_sales_json/",
            method: "GET",
            contentType: "application/json",
            beforeSend: function () {
                const load = $('.loading-message-weekly')
                load.addClass('loading-message');
            },
            success: function (data) {
                const load = $('.loading-message-weekly')
                load.removeClass('loading-message');

                Object.keys(data).forEach(day => {
                    let salesData = data[day];
                    let total = salesData.length;
                    nums.push(total);
                });

                if (weeklySalesChart === null) {
                    weeklySalesChart = new Chart(weeklyCtx, {
                        type: chartType,
                        data: {
                            labels: labelsList,
                            datasets: [{
                                label: "This week",
                                data: nums,
                                backgroundColor: ["brown"],
                                borderColor: ["rgb(47, 79, 79, 0.7)"],
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
                                    text: 'Weekly Sales Analysis',
                                    color: 'navy',
                                    position: 'bottom',
                                    align: 'center',
                                    font: {
                                        weight: 'bold'
                                    },
                                    padding: 8,
                                    fullSize: true,
                                },
                                dataLabels: {
                                    formatter: (value) => {
                                        return value + '%';
                                    }

                                },
                            }
                        }
                    });
                } else {
                    weeklySalesChart.data.labels = labelsList;
                    weeklySalesChart.data.datasets[0].data = nums;
                    weeklySalesChart.update();
                }
                setTimeout(fetchAndUpdateWeeklyData, 5 * 60 * 1000);
            },
            error: function (err) {
                console.error(err);
            }
        });
    }
    fetchAndUpdateWeeklyData();
}
updateWeeklyChart();



function updateSalesByAgentChart() {
    if (salesByAgentChart === null) {
        salesByAgentCtx = $('.sales_by_agent_chart').get(0).getContext('2d');
    }
    let date = new Date();
    let chartType = "bar";
    
    function fetchAndUpdateAgentMonthly() {
        let labelsList = [];
        let nums = [];

        $.ajax({
            url: "/system_core_1/get_sale_by_agent_monthy/",
            method: "GET",
            contentType: "application/json",
            beforeSend: function () {
                const load = $('.loading-message-monthly')
                load.addClass('loading-message');
            },
            success: function (data) {
                const load = $('.loading-message-monthly')
                load.removeClass('loading-message');

                const totalData = data.find(item => item[0] === "Total");
                const total = totalData ? totalData[1] : 0;
                const filteredData = data.filter(item => item[0] !== "Total");
                labelsList = filteredData.map(item => item[0]);
                nums = filteredData.map(item => item[1]);

                if (salesByAgentChart === null) {
                    salesByAgentChart = new Chart(salesByAgentCtx, {
                        type: chartType,
                        data: {
                            labels: labelsList,
                            datasets: [{
                                label: months[date.getMonth()] + " Total Sales " + `${total}`,
                                data: nums,
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
                                    text: 'Sales by Agents',
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
                            indexAxis: 'y',
                            barPercentage: 0.7,
                            categoryPercentage: 0.7
                        }
                    });
                } else {
                    salesByAgentChart.data.labels = labelsList;
                    salesByAgentChart.data.datasets[0].data = nums;
                    salesByAgentChart.data.datasets[0].label = months[date.getMonth()] + " Total Sales " + `${total}`;
                    salesByAgentChart.update();
                }
                setTimeout(fetchAndUpdateAgentMonthly, 5 * 60 * 1000);
            },
            error: function (err) {
                console.error(err);
            }
        });
    }
    fetchAndUpdateAgentMonthly();
}

updateSalesByAgentChart();
