let agent_stockChart = null;
let agent_stockctx = null;

function agent_stock_chart_details() {
  if (agent_stockChart === null) {
    agent_stockctx = $('.StockChart').get(0).getContext('2d');
  }

  const date = new Date();
  const chartType = 'doughnut';

  function fetchAndUpdateDailyData() {
    const modelList = [];
    const total = [];
    const colors = [];

    $.ajax({
      url: '/system_core_1/get_individual_agent_stock/',
      method: 'GET',
      contentType: 'application/json',
      beforeSend() {
        const load = $('.loading-message-agent-stock');
        load.addClass('loading-message');
      },
      success(data) {
        const load = $('.loading-message-agent-stock');
        load.removeClass('loading-message');

        $.each(data, (model, value) => {
          modelList.push(model);
          total.push(value);
        });

        for (let i = 0; i < modelList.length; i++) {
          const num1 = Math.round(Math.random() * 255 + 1);
          const num2 = Math.round(Math.random() * 255 + 1);
          const num3 = Math.round(Math.random() * 255 + 1);
          colors.push(`rgb(${num1}, ${num2}, ${num3})`);
        }

        if (agent_stockChart === null) {
          agent_stockChart = new Chart(agent_stockctx, {
            type: chartType,
            data: {
              labels: modelList,
              datasets: [{
                label: date.toDateString(),
                data: total,
                backgroundColor: colors,
                borderColor: colors,
                borderWidth: 2,
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
                  text: 'Stock Analysis',
                  color: 'navy',
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
                    color: 'black',
                    font: {
                      size: 8,
                      weight: 'bold',
                    },
                  },
                },
              },
            },
          });
        } else {
          agent_stockChart.data.labels = labelsList;
          agent_stockChart.data.datasets[0].data = total;
          agent_stockChart.update();
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
agent_stock_chart_details();

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


const dest_daily_3 = '.dailySalesChart';
const url_daily_3 = '/system_core_1/agent_daily_sales/';
const loader_daily_3 = '.loading-message-Daily-Sales';

updateDailyChart(url_daily_3, dest_daily_3, 'bar', loader_daily_3);