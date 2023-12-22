
/**
 * updateWeeklyChart - Fetches data from the server and renders a chart on the canvas element
 * @param {*} dest - The canvas element to render the chart
 * @param {*} url - The url to fetch the data from
 * @param {*} chartType - The type of chart to render
 * @param {*} loader - The loader element to show when fetching data
 */
function updateWeeklyChart(url, dest, chartType = "line", loader) {
    let weeklySalesChart = null;
    let weeklyCtx = null;

    if (weeklySalesChart === null) {
        weeklyCtx = $(dest).get(0).getContext('2d');
    }
    
    let labelsList = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

    function fetchAndUpdateWeeklyData() {
        let nums = [];
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

                Object.keys(data).forEach(day => {
                    let salesData = data[day];
                    let total = salesData.length;
                    nums.push(total);
                    overallTotal += total;
                });

                if (weeklySalesChart === null) {
                    weeklySalesChart = new Chart(weeklyCtx, {
                        type: chartType,
                        data: {
                            labels: labelsList,
                            datasets: [{
                                label: "This week's total " + overallTotal,
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

const dest_1 = ".Weekly_sales_chart_loan";
const url_1 = "/system_core_1/get_weekly_sales_json_loan/";
const loader_1 = ".weekly_sales_loader_loan";
const dest_2 = ".Weekly_sales_chart_cash";
const url_2 = "/system_core_1/get_weekly_sales_json_cash/";
const loader_2 = ".weekly_sales_loader_cash";

updateWeeklyChart(url_1, dest_1, "line", loader_1);
updateWeeklyChart(url_2, dest_2, "line", loader_2);