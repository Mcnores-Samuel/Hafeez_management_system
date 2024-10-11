function dailyUpdateByShop(url, dest, chartType) {
    let dailySalesChartD = null;
    let dailyCtx = null;
  
    if (dailySalesChartD === null) {
      dailyCtx = $(dest).get(0).getContext('2d');
    }
  
    const date = new Date();
  
    function fetchAndUpdateDailyData() {
      const modelList = [];
      const total = [];
      let overallTotal = 0;
  
      $.ajax({
        url,
        method: 'GET',
        contentType: 'application/json',
        success(data) {
          $.each(data.data, (index, item) => {
            modelList.push(item.shop);
            total.push(item.total_sales);
            overallTotal += item.total_sales;
          });
  
          if (dailySalesChartD === null) {
            dailySalesChartD = new Chart(dailyCtx, {
              type: chartType,
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
          setTimeout(fetchAndUpdateDailyData, 5 * 60 * 1000);
        },
        error(err) {
          console.error(err);
        },
      });
    }
    fetchAndUpdateDailyData();
  }

const url = '/system_core_1/dailySalesByShop';
const dest = '.overall_daily_sales';
const chartType = 'bar';

dailyUpdateByShop(url, dest, chartType, loader);