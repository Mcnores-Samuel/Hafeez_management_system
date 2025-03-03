let dailySalesChartD = null;
let monthlySalesChartD = null;
let stockChartD = null;

function dailySalesChart(data, dateobj) {
    const dailyCtx = $('.daily_sales').get(0).getContext('2d');  // Get the canvas context

    // Destroy the chart if it already exists
    if (dailySalesChartD !== null) {
        dailySalesChartD.destroy();
    }

    const modelList = [];
    const total = [];
    let overallTotal = 0;

    const date = new Date(dateobj);

    // Populate modelList and total
    $.each(data, (model, value) => {
        modelList.push(model);
        total.push(value);
        overallTotal += value;
    });

    // Create the chart
    dailySalesChartD = new Chart(dailyCtx, {
        type: 'bar',
        data: {
            labels: modelList,
            datasets: [{
                label: `${date.toDateString()} Total ${overallTotal}`,
                data: total,
                backgroundColor: '#2980B9', // Blue color
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // Allows for better chart scaling
            events: ['mousemove'],
            interaction: {
                mode: 'nearest',
            },
            plugins: {
                title: {
                    display: true,
                    text: `Daily Sales: ${overallTotal}`,
                    color: '#fe9a43', // Darker blue color
                    position: 'bottom',
                    align: 'center',
                    font: {
                        weight: 'bold',
                        size: 16, // Adjust font size
                    },
                    padding: 10, // Adjust padding for spacing
                    fullSize: true,
                },
            },
            scales: {
                x: {
                    grid: {
                        display: false, // Hide grid lines
                    },
                    ticks: {
                        color: '#fe9a43', // Darker blue color
                        font: {
                            weight: 'bold', // Regular font weight
                        },
                    },
                },
                y: {
                    grid: {
                        display: false, // Hide grid lines
                    },
                    ticks: {
                        color: '#fe9a43', // Darker blue color
                        font: {
                            weight: 'bold', // Regular font weight
                        },
                    },
                },
            },
        },
    });
}

function monthlySalesChart(data, year, monthObj) {
    const monthlyCtx = $('.monthly_sales').get(0).getContext('2d');  // Get the canvas context

    // Destroy the chart if it already exists
    if (monthlySalesChartD !== null) {
        monthlySalesChartD.destroy();
    }

    const modelList = [];
    const total = [];
    let overallTotal = 0;

    const month = new Date(year, monthObj - 1).toLocaleString(
        'default', { month: 'long', year: 'numeric' });

    // Populate modelList and total
    $.each(data, (model, value) => {
        modelList.push(model);
        total.push(value);
        overallTotal += value;
    });

    // Create the chart
    monthlySalesChartD = new Chart(monthlyCtx, {
        type: 'bar',
        data: {
            labels: modelList,
            datasets: [{
                label: `${month} Total ${overallTotal}`,
                data: total,
                backgroundColor: '#2980B9', // Blue color
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // Allows for better chart scaling
            events: ['mousemove'],
            interaction: {
                mode: 'nearest',
            },
            plugins: {
                title: {
                    display: true,
                    text: `Monthly Sales: ${overallTotal}`,
                    color: '#fe9a43', // Darker blue color
                    position: 'bottom',
                    align: 'center',
                    font: {
                        weight: 'bold',
                        size: 16, // Adjust font size
                    },
                    padding: 10, // Adjust padding for spacing
                    fullSize: true,
                },
            },
            scales: {
                x: {
                    grid: {
                        display: false, // Hide grid lines
                    },
                    ticks: {
                        color: '#fe9a43', // Darker blue color
                        font: {
                            weight: 'bold', // Regular font weight
                        },
                    },
                },
                y: {
                    grid: {
                        display: false, // Hide grid lines
                    },
                    ticks: {
                        color: '#fe9a43', // Darker blue color
                        font: {
                            weight: 'bold', // Regular font weight
                        },
                    },
                },
            },
        },
    });
}

function stockChart(data) {
    const stockCtx = $('.stock').get(0).getContext('2d');  // Get the canvas context

    // Destroy the chart if it already exists
    if (stockChartD !== null) {
        stockChartD.destroy();
    }

    const modelList = [];
    const total = [];
    let overallTotal = 0;
    const color = []

    // Populate modelList and total
    $.each(data, (model, value) => {
        modelList.push(model);
        total.push(value);
        overallTotal += value;
    });

    for (let i = 0; i < modelList.length; i++) {
        color.push('#' + Math.floor(Math.random()*16777215).toString(16));
    }

    // Create the chart
    stockChartD = new Chart(stockCtx, {
        type: 'doughnut',
        data: {
            labels: modelList,
            datasets: [{
                label: `Total ${overallTotal}`,
                data: total,
                backgroundColor: color,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // Allows for better chart scaling
            plugins: {
                title: {
                    display: true,
                    text: `Stock: ${overallTotal}`,
                    color: '#fe9a43', // Darker blue color
                    position: 'bottom',
                    align: 'center',
                    font: {
                        weight: 'bold',
                        size: 16, // Adjust font size
                    },
                    padding: 10, // Adjust padding for spacing
                    fullSize: true,
                },
                legend: {
                    display: false,
                },
            },
        },
    });
}

export { dailySalesChart, monthlySalesChart, stockChart };