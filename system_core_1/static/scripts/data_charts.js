const months = [
    "January", "February", 
    "March", "April", "May", 
    "June", "July", "August",
    "September", "October", 
    "November", "December"
];

let monthly_ctx = null;
let monthly_chart = null;
let weekly_sales_chart = null;
let weekly_ctx = null;
let daily_sales_chart = null;
let daily_ctx = null;


function update_monthly_Chart() {
    if (monthly_chart === null) {
        monthly_ctx = document.querySelector('.products').getContext('2d');
    }
    
    let date = new Date()
    let labels_list = []
    let nums = []
    let chart_type = "line"
    
    fetch("/get_models_json/")
    .then(response => response.json())
    .then(data => {
        for(let i = 0; i < data.length; i++) {
            if (data.length > 20){
                chart_type = "line"
            }
            labels_list.push(data[i].type)
            nums.push(data[i].total)
        }
        
        if (monthly_chart === null) {
            monthly_chart = new Chart(monthly_ctx, {
                type: chart_type,
                data: {
                    labels: labels_list,
                    datasets: [{
                        label: months[date.getMonth()] + " Data",
                        data: nums,
                        backgroundColor: ["#000C66", "blue", "green", "yellow", "gray"],
                        borderColor: ["#000C66", "blue", "green", "yellow", "gray"],
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
                           text: 'Monthy Inventory Analysis',
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
            monthly_chart.data.labels = labels_list;
            monthly_chart.data.datasets[0].data = nums;
            monthly_chart.update();
        }
    })
    .catch(err => console.error(err));
}

function update_daily_Chart() {
    if (daily_sales_chart === null) {
        daily_ctx = document.querySelector('.daily_sales_chart').getContext('2d');
    }
    
    let date = new Date()
    let chart_type = "line"

    function fetch_and_update_daily_data() {
            let model_list = []
            let total = []
        fetch("/system_core_1/get_daily_sales_json/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        })
        .then(response => response.json())
        .then(data => {
            Object.keys(data).forEach(model => {
                model_list.push(model)
                total.push(data[model])
            });
            
            if (daily_sales_chart === null) {
                daily_sales_chart = new Chart(daily_ctx, {
                    type: chart_type,
                    data: {
                        labels: model_list,
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
                daily_sales_chart.data.labels = labels_list;
                daily_sales_chart.data.datasets[0].data = nums;
                daily_sales_chart.update();
            }
            setTimeout(fetch_and_update_daily_data, 10000 * 60);
        })
        .catch(err => console.error(err));
    }
    fetch_and_update_daily_data();
}

update_daily_Chart();


function update_weekly_Chart() {
    if (weekly_sales_chart === null) {
        weekly_ctx = document.querySelector('.Weekly_sales_chart').getContext('2d');
    }
    let labels_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    let chart_type = "line"

    function fetch_and_update_weekly_data() {
        let nums = []
        fetch("/system_core_1/get_weekly_sales_json/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        
        })
        .then(response => response.json())
        .then(data => {
            Object.keys(data).forEach(day => {
                let salesData = data[day]
                let total = salesData.length
                nums.push(total)
            });

            if (weekly_sales_chart === null) {
                weekly_sales_chart = new Chart(weekly_ctx, {
                    type: chart_type,
                    data: {
                        labels: labels_list,
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
                            }
                        }
                    }
                });
            } else {
                weekly_sales_chart.data.labels = labels_list;
                weekly_sales_chart.data.datasets[0].data = nums;
                weekly_sales_chart.update();
            }
            setTimeout(fetch_and_update_weekly_data, 10000 * 60);
        })
        .catch(err => console.error(err));
    }
    fetch_and_update_weekly_data();
}
update_weekly_Chart();



let sales_by_agent_chart = null;
let sales_by_agent_ctx = null;

function update_sales_by_agent_Chart() {
    if (sales_by_agent_chart === null) {
        sales_by_agent_ctx = document.querySelector('.sales_by_agent_chart').getContext('2d');
    }
    let date = new Date()
    let chart_type = "bar"

    function fetch_and_update_agent_monthly() {
        let labels_list = []
        let nums = []
        fetch("/system_core_1/get_sale_by_agent_monthy/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        
        })
        .then(response => response.json())
        .then(data => {
            Object.keys(data).forEach(agent => {
                labels_list.push(agent)
                nums.push(data[agent])
                console.log(data[agent])
            });

            if (sales_by_agent_chart === null) {
                sales_by_agent_chart = new Chart(sales_by_agent_ctx, {
                    type: chart_type,
                    data: {
                        labels: labels_list,
                        datasets: [{
                            label: months[date.getMonth()] + " Data",
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
                            text: 'Sales by Agent',
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
                        barPercentage: 0.6,
                        categoryPercentage: 0.6
                    }
                });
            } else {
                sales_by_agent_chart.data.labels = labels_list;
                sales_by_agent_chart.data.datasets[0].data = nums;
                sales_by_agent_chart.update();
            }
            setTimeout(fetch_and_update_agent_monthly, 10000 * 60);
        })
        .catch(err => console.error(err));
    }
    fetch_and_update_agent_monthly();
}
update_sales_by_agent_Chart();
