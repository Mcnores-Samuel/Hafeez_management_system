function updateDailyChart(url, dest, chartType, loader) {
  let dailySalesChart = null;
  let dailyCtx = null;

  if (dailySalesChart === null) {
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
      beforeSend() {
        const load = $(loader);
        load.addClass('loading-message');
      },
      success(data) {
        const load = $(loader);
        load.removeClass('loading-message');

        $.each(data, (model, value) => {
          modelList.push(model);
          total.push(value);
          overallTotal += value;
        });

        if (dailySalesChart === null) {
          dailySalesChart = new Chart(dailyCtx, {
            type: chartType,
            data: {
              labels: modelList,
              datasets: [{
                label: `${date.toDateString()} Total ${overallTotal}`,
                data: total,
                backgroundColor: 'rgba(54, 162, 235, 0.6)', // Blue color
                borderColor: 'rgba(54, 162, 235, 1)', // Blue color
                borderWidth: 2,
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
                  text: `Daily approved contracts: ${overallTotal}`,
                  color: '#fe9a43', // Darker blue color
                  position: 'bottom',
                  align: 'center',
                  font: {
                    weight: 'bold',
                    size: 16,
                  },
                  padding: 10, // Adjust padding for spacing
                  fullSize: true,
                },
              },
              scales: {
                x: {
                  grid: {
                    display: false, // No grid lines
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
                    display: false, // No grid lines
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
        } else {
          dailySalesChart.data.labels = modelList;
          dailySalesChart.data.datasets[0].data = total;
          dailySalesChart.update();
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

const dailySalesUrl = '/system_core_1/daily_approved_contracts/';
const dailySalesDest = '.daily_approved_contracts_chart';
const dailySalesChartType = 'bar';
const dailySalesLoader = '.daily_sales_loader';

updateDailyChart(dailySalesUrl, dailySalesDest, dailySalesChartType, dailySalesLoader);
