function dailyMetricsChart(data) {
    let dailyCollectionsChart = null;
    if (dailyCollectionsChart !== null) {
        dailyCollectionsChart.destroy();
    }

    const dailyDataCtx = $('.dailyCollectionsChart').get(0).getContext('2d');
    const modelList = [];
    const total = [];

    data.forEach(function(item) {
        if (item.todays_collection > 0) {
            modelList.push(item.promoter.first_name + ' ' + item.promoter.last_name);
            total.push(item.todays_collection);
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
                    text: 'Daily Collections',
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