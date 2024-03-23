/**
 * updateDailyChart - Fetches the data from the url and renders the chart
 * @param {*} url - The url to fetch the data from
 * @param {*} dest - The canvas element to render the chart
 * @param {*} chartType - The type of chart to render
 * @param {*} loader - The loader element to show when fetching data
 */
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
                backgroundColor: ['navy'],
                borderColor: ['navy'],
                borderWidth: 2,
              }],
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              events: ['mousemove'],
              interaction: {
                mode: 'nearest',
              },
              plugins: {
                title: {
                  display: true,
                  text: 'Daily Sales Analysis',
                  color: 'navy',
                  position: 'bottom',
                  align: 'center',
                  font: {
                    weight: 'bold',
                  },
                  padding: 8,
                  fullSize: true,
                },
              },
              scales: {
                x: {
                  grid: {
                    display: false,
                  },
                  ticks: {
                    color: 'navy',
                    font: {
                      weight: 'bold',
                    },
                  },
                },
                y: {
                  grid: {
                    display: false,
                  },
                  ticks: {
                    color: 'navy',
                    font: {
                      weight: 'bold',
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

const dest_daily = '.daily_sales_chart_loan';
const url_daily = '/system_core_1/get_daily_sales_json_loan/';
const loader_daily = '.daily_sales_loader_loan';
const dest_daily_2 = '.daily_sales_chart_cash';
const url_daily_2 = '/system_core_1/get_daily_sales_json_cash/';
const loader_daily_2 = '.daily_sales_loader_cash';

updateDailyChart(url_daily, dest_daily, 'bar', loader_daily);
updateDailyChart(url_daily_2, dest_daily_2, 'bar', loader_daily_2);
