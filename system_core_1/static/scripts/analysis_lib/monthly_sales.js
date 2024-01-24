const months = [
    "January", "February", 
    "March", "April", "May", 
    "June", "July", "August",
    "September", "October", 
    "November", "December"
];

function updateSalesByAgentChart(url, dest, chartType, loader) {
    let salesByAgentChart = null;
    let salesByAgentCtx = null;

    if (salesByAgentChart === null) {
        salesByAgentCtx = $(dest).get(0).getContext('2d');
    }
    let date = new Date();
    
    function fetchAndUpdateAgentMonthly() {
        let labelsList = [];
        let nums = [];

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
                                label: months[date.getMonth()] + " Total loan Sales " + `${total}`,
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
                                    text: months[date.getMonth()] + " Sales Analysis",
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
                            categoryPercentage: 0.7,
                            scales: {
                                x: {
                                    grid: {
                                        display: false
                                    },

                                    ticks: {
                                        beginAtZero: true,
                                        stepSize: 1,
                                        color: "navy",
                                        font: {
                                            weight: 'bold'
                                        },
                                    }
                                },
                                y: {
                                    grid: {
                                        display: false
                                    },
                                    ticks: {
                                        color: "navy",
                                        font: {
                                            weight: 'bold'
                                        },
                                    },
                                }
                            }
                        }
                    });
                } else {
                    salesByAgentChart.data.labels = labelsList;
                    salesByAgentChart.data.datasets[0].data = nums;
                    salesByAgentChart.data.datasets[0].label = months[date.getMonth()] + " Total loan Sales " + `${total}`;
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

const dest_monthly = ".agent_sales_loan_chart";
const url_monthly = "/system_core_1/get_sale_by_agent_monthy_loan/"
const loader_monthly = ".agent_sales_loan_chart_loader";
const dest_monthly2 = ".agent_sales_cash_chart";
const url_monthly2 = "/system_core_1/get_sale_by_agent_monthy_cash/"
const loader_monthly2 = ".agent_sales_cash_chart_loader";


updateSalesByAgentChart(url_monthly, dest_monthly,
    "bar", loader_monthly);
updateSalesByAgentChart(url_monthly2, dest_monthly2,
    "bar", loader_monthly2);