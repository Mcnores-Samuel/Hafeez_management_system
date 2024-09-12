function dailyMetricsChart(data) {
    let dailyCollectionsChart = null;
    if (dailyCollectionsChart !== null) {
        dailyCollectionsChart.destroy();
    }

    const dailyDataCtx = $('.dailyCollectionsChart').get(0).getContext('2d');
    const modelList = [];
    const total = [];
    let grandTotal = 0;

    data.forEach(function(item) {
        if (item.todays_collection > 0) {
            modelList.push(item.promoter.first_name + ' ' + item.promoter.last_name);
            total.push(item.todays_collection);
            grandTotal += item.todays_collection;
        }
    });

    dailyCollectionsChart = new Chart(dailyDataCtx, {
        type: 'bar',
        data: {
            labels: modelList,
            datasets: [{
                label: 'Daily Collections',
                data: total,
                backgroundColor: '#2980B9'
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `Total: ${grandTotal}`,
                    color: '#fe9a43',
                    position: 'bottom',
                    align: 'center',
                    font: {
                        weight: 'bold',
                        size: 16
                    },
                    padding: 10,
                    fullSize: true
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false, // Hide grid lines
                    },
                    ticks: {
                        color: '#fe9a43', // Color for x-axis labels
                        font: {
                            weight: 'bold', // Font weight
                        },
                    },
                },
                y: {
                    grid: {
                        display: false, // Hide grid lines
                    },
                    ticks: {
                        color: '#fe9a43', // Color for y-axis labels
                        font: {
                            weight: 'bold', // Font weight
                        },
                    },
                }
            }
        }
    });
}

function availableStock(data) {
    let availableStockChart = null;
    if (availableStockChart !== null) {
        availableStockChart.destroy();
    }

    const availableStockCtx = $('.available_stock_chart').get(0).getContext('2d');
    const modelList = [];
    const total = [];
    let grandTotal = 0;
    const colors = [];

    data.forEach(function(item) {
        console.log(item);
        if (item.available_stock) {
            if (item.available_stock.mifi === 'MIFI') {
                modelList.push(item.available_stock.mifi);
                total.push(item.available_stock.total_mifi);
                grandTotal += item.available_stock.total_mifi;
            }
            if (item.available_stock.idu === 'IDU') {
                modelList.push(item.available_stock.idu);
                total.push(item.available_stock.total_idu);
                grandTotal += item.available_stock.total_idu;
            }
        }
    });

    for (let i = 0; i < modelList.length; i++) {
        const num1 = Math.round(Math.random() * 255 + 1);
        const num2 = Math.round(Math.random() * 255 + 1);
        const num3 = Math.round(Math.random() * 255 + 1);
        colors.push(`rgb(${num1}, ${num2}, ${num3})`);
    }

    availableStockChart = new Chart(availableStockCtx, {
        type: 'doughnut',
        data: {
            labels: modelList,
            datasets: [{
                label: 'Available Stock',
                data: total,
                backgroundColor: colors,
                borderColor: colors,
                borderWidth: 2
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
              animateScale: true,
              animateRotate: true,
            },
            events: ['mousemove'],
            interaction: {
              mode: 'nearest',
            },
            plugins: {
              title: {
                display: true,
                text: `Total available stock: ${grandTotal}`,
                color: '#fe9a43',
                position: 'bottom',
                align: 'center',
                font: {
                  weight: 'bold',
                },
                padding: 8,
                fullSize: true,
              },
              legend: {
                display: true,
                position: 'right',
                labels: {
                  color: '#fe9a43',
                  font: {
                    size: 10,
                    weight: 'bold',
                  },
                },
              },
            },
        },
    });
}


export { dailyMetricsChart, availableStock };