let cash_sales_Chart = null;
let cash_sales_ctx = null;

function cash_sales_analysis() {
    if (cash_sales_Chart === null) {
        cash_sales_ctx = $('.cash_sales_analysis').get(0).getContext('2d');
    }
    let date = new Date();
    let chartType = "bar";
    
    function fetchAndUpdateAgentMonthly() {
        let labelsList = [];
        let nums = [];

        $.ajax({
            url: "/system_core_1/get_sale_by_agent_monthy_cash/",
            method: "GET",
            contentType: "application/json",
            beforeSend: function () {
                const load = $('.loading-message-monthly-cash')
                load.addClass('loading-message');
            },
            success: function (data) {
                const load = $('.loading-message-monthly-cash')
                load.removeClass('loading-message');

                const totalData = data.find(item => item[0] === "Total");
                const total = totalData ? totalData[1] : 0;
                const filteredData = data.filter(item => item[0] !== "Total");
                labelsList = filteredData.map(item => item[0]);
                nums = filteredData.map(item => item[1]);

                if (cash_sales_Chart === null) {
                    cash_sales_Chart = new Chart(cash_sales_ctx, {
                        type: chartType,
                        data: {
                            labels: labelsList,
                            datasets: [{
                                label: months[date.getMonth()] + " Total Cash Sales " + `${total}`,
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
                            categoryPercentage: 0.7
                        }
                    });
                } else {
                    cash_sales_Chart.data.labels = labelsList;
                    cash_sales_Chart.data.datasets[0].data = nums;
                    cash_sales_Chart.data.datasets[0].label = months[date.getMonth()] + " Total Cash Sales " + `${total}`;
                    cash_sales_Chart.update();
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

cash_sales_analysis();