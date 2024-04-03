function yearly_sales_analysis(url, dest, chartType, loader) {
  let sales_analystChart = null;
  let yearly_analysisctx = null;

  if (sales_analystChart === null) {
    yearly_analysisctx = $(dest).get(0).getContext('2d');
  }

  const date = new Date();

  function fetchAndUpdateDailyData() {
    const modelList = [];
    const total = [];

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

        $.each(data, (key, value) => {
          modelList.push(key);
          total.push(value);
        });

        if (sales_analystChart === null) {
          sales_analystChart = new Chart(yearly_analysisctx, {
            type: chartType,
            data: {
              labels: modelList,
              datasets: [{
                label: date.toDateString(),
                data: total,
                backgroundColor: '#4285F4',
                borderColor: '#4285F4',
                borderWidth: 2,
              }],
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                title: {
                  display: true,
                  text: `Yearly Sales Analysis: Total Sales: ${total.reduce((a, b) => a + b, 0)}`,
                  color: '#333',
                  position: 'bottom',
                  align: 'center',
                  font: {
                    weight: 'bold',
                    size: 16,
                  },
                  padding: 20,
                },
                legend: {
                  display: false,
                },
              },
              scales: {
                x: {
                  grid: {
                    display: false,
                    drawBorder: false,
                  },
                  ticks: {
                    color: '#333',
                    font: {
                      weight: 'bold',
                    },
                  },
                },
                y: {
                  grid: {
                    display: false,
                    drawBorder: false,
                  },
                  ticks: {
                    color: '#333',
                    font: {
                      weight: 'bold',
                    },
                  },
                },
              },
            },
          });
        } else {
          sales_analystChart.data.labels = labelsList;
          sales_analystChart.data.datasets[0].data = total;
          sales_analystChart.update();
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

function yearly_sales_analysis_product(url, dest, chartType, loader) {
  let sales_analystChart_pro = null;
  let yearly_analysisctx_pro = null;

  if (sales_analystChart_pro === null) {
    yearly_analysisctx_pro = $(dest).get(0).getContext('2d');
  }

  const date = new Date();

  function fetchAndUpdateDailyData() {
    let modelList = [];
    let total = [];

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

        modelList = data.map((item) => item[0]);
        total = data.map((item) => item[1]);

        if (sales_analystChart_pro === null) {
          sales_analystChart_pro = new Chart(yearly_analysisctx_pro, {
            type: chartType,
            data: {
              labels: modelList,
              datasets: [{
                label: date.toDateString(),
                data: total,
                backgroundColor: '#4285F4',
                borderColor: '#4285F4',
                borderWidth: 2,
              }],
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                title: {
                  display: true,
                  text: 'Yearly Sales Analysis by Product',
                  color: '#333',
                  position: 'bottom',
                  align: 'center',
                  font: {
                    weight: 'bold',
                    size: 16,
                  },
                  padding: 20,
                },
                legend: {
                  display: false,
                },
              },
              scales: {
                x: {
                  grid: {
                    display: false,
                    drawBorder: false,
                  },
                  ticks: {
                    color: '#333',
                    font: {
                      weight: 'bold',
                    },
                  },
                },
                y: {
                  grid: {
                    display: false,
                    drawBorder: false,
                  },
                  ticks: {
                    color: '#333',
                    font: {
                      weight: 'bold',
                    },
                  },
                },
              },
            },
          });
        } else {
          sales_analystChart_pro.data.labels = labelsList;
          sales_analystChart_pro.data.datasets[0].data = total;
          sales_analystChart_pro.update();
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

const url_yearly = '/system_core_1/get_yearly_sales/';
const dest_yearly = '.yearly_sales_chart';
const chartType_yearly = 'bar';
const loader_yearly = '.yearly_sales_chart_loader';

const product_analysis = '/system_core_1/get_yearly_product_sales/';
const product_dest = '.yearly_product_sales_chart';
const product_loader = '.yearly_product_sales_chart_loader';
const chartType_product = 'bar';

const urlYearlyOther = '/system_core_1/get_yearly_sales_total/';
const destYearlyOther = '.yearly_sales_chart_total';
const chartTypeYearlyOther = 'bar';
const loaderYearlyOther = '.yearly_sales_chart_loader_total';


yearly_sales_analysis(
  url_yearly, dest_yearly,
  chartType_yearly, loader_yearly,
);

yearly_sales_analysis(
  urlYearlyOther, destYearlyOther,
  chartTypeYearlyOther, loaderYearlyOther,
);
yearly_sales_analysis_product(
  product_analysis, product_dest,
  chartType_product, product_loader,
);
