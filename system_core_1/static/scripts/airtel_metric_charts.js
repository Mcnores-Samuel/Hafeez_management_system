function dailyMetricsChart(data) {
    let dailyCollectionsChart = null;
    if (dailyCollectionsChart !== null) {
        dailyCollectionsChart.destroy();
    }

    const dailyDataCtx = $('.dailyCollectionsChart').get(0).getContext('2d');
    const modelList = [];
    const iduTotals = [];
    const mifiTotals = [];
    let grandTotal = 0;

    data.forEach(function(item) {
        if (item.todays_idu_collection > 0 || item.todays_mifi_collection > 0) {
            modelList.push(item.promoter.first_name + ' ' + item.promoter.last_name);
            iduTotals.push(item.todays_idu_collection); // IDU collection
            mifiTotals.push(item.todays_mifi_collection); // MIFI collection
            grandTotal += item.todays_idu_collection + item.todays_mifi_collection;
        }
    });

    dailyCollectionsChart = new Chart(dailyDataCtx, {
        type: 'bar',
        data: {
            labels: modelList,
            datasets: [
                {
                    label: 'IDU Collections',
                    data: iduTotals,
                    backgroundColor: '#2980B9'
                },
                {
                    label: 'MIFI Collections',
                    data: mifiTotals,
                    backgroundColor: '#E74C3C'
                }
            ],
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
                    stacked: true, // Enable stacking for x-axis
                    grid: {
                        display: false,
                    },
                    ticks: {
                        color: '#fe9a43',
                        font: {
                            weight: 'bold',
                        },
                    },
                },
                y: {
                    stacked: true, // Enable stacking for y-axis
                    grid: {
                        display: false,
                    },
                    ticks: {
                        color: '#fe9a43',
                        font: {
                            weight: 'bold',
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

function dailyPaymentsChart(data) {
    let dailyPaymentsChart = null;
    if (dailyPaymentsChart !== null) {
        dailyPaymentsChart.destroy();
    }

    const dailyPaymentsCtx = $('.dailyPaymentsChart').get(0).getContext('2d');
    const modelList = [];
    const iduTotals = [];
    const mifiTotals = [];
    let grandTotal = 0;

    data.forEach(function(item) {
        if (item.todays_idu_payments > 0 || item.todays_mifi_payments > 0) {
            modelList.push(item.promoter.first_name + ' ' + item.promoter.last_name);
            iduTotals.push(item.todays_idu_payments); // IDU collection
            mifiTotals.push(item.todays_mifi_payments); // MIFI collection
            grandTotal += item.todays_idu_payments + item.todays_mifi_payments;
        }
    });

    dailyPaymentsChart = new Chart(dailyPaymentsCtx, {
        type: 'bar',
        data: {
            labels: modelList,
            datasets: [
                {
                    label: 'IDU Payments',
                    data: iduTotals,
                    backgroundColor: '#2980B9'
                },
                {
                    label: 'MIFI Payments',
                    data: mifiTotals,
                    backgroundColor: '#E74C3C'
                }
            ],
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
                },
                legend: {
                    display: false,
                }
            },
            scales: {
                x: {
                    stacked: true, // Enable stacking for x-axis
                    grid: {
                        display: false,
                    },
                    ticks: {
                        color: '#fe9a43',
                        font: {
                            weight: 'bold',
                        },
                    },
                },
                y: {
                    stacked: true, // Enable stacking for y-axis
                    grid: {
                        display: false,
                    },
                    ticks: {
                        color: '#fe9a43',
                        font: {
                            weight: 'bold',
                        },
                    },
                }
            }
        }
    });
}

function stockByIndividuals(data) {
    let stockByIndividualsChart = null;
    if (stockByIndividualsChart !== null) {
        stockByIndividualsChart.destroy();
    }

    const stockByIndividualsCtx = $('.stockByIndividualsChart').get(0).getContext('2d');
    const modelList = [];
    const totalStocks = []; // Total IDU + MIFI stock
    const iduTotals = [];
    const mifiTotals = [];
    let grandTotal = 0;

    // Function to generate random colors
    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    // Create a color list for all individuals
    const backgroundColors = [];

    data.forEach(function(item) {
        if (item.idu_stock > 0 || item.mifi_stock > 0) {
            modelList.push(item.promoter.first_name + ' ' + item.promoter.last_name);
            const totalStock = item.idu_stock + item.mifi_stock;
            totalStocks.push(totalStock); // Total for doughnut chart
            iduTotals.push(item.idu_stock);
            mifiTotals.push(item.mifi_stock);
            grandTotal += totalStock;

            // Generate random color for each individual and push it to the list
            backgroundColors.push(getRandomColor());
        }
    });

    stockByIndividualsChart = new Chart(stockByIndividualsCtx, {
        type: 'doughnut',
        data: {
            labels: modelList,
            datasets: [
                {
                    label: 'Total Stock',
                    data: totalStocks, // Total IDU + MIFI per individual
                    backgroundColor: backgroundColors, // Use the generated random colors
                    borderColor: '#FFFFFF',
                    borderWidth: 2
                }
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        // Custom tooltip to show IDU and MIFI breakdown
                        label: function(context) {
                            const index = context.dataIndex;
                            const idu = iduTotals[index];
                            const mifi = mifiTotals[index];
                            return `${context.label}: Total: ${totalStocks[index]}, IDU: ${idu}, MIFI: ${mifi}`;
                        }
                    }
                },
                title: {
                    display: true,
                    text: `Total Stock: ${grandTotal}`,
                    color: '#fe9a43',
                    position: 'bottom',
                    align: 'center',
                    font: {
                        weight: 'bold',
                        size: 16
                    },
                    padding: 10,
                    fullSize: true
                },
                legend: {
                    display: false // Hide the legend
                }
            }
        }
    });
}

export { dailyMetricsChart, availableStock,
    dailyPaymentsChart, stockByIndividuals };