const months = [
  'January', 'February',
  'March', 'April', 'May',
  'June', 'July', 'August',
  'September', 'October',
  'November', 'December',
];

function updateSalesByAgentChart(url, dest, chartType, loader) {
  let salesByAgentChart = null;
  let salesByAgentCtx = null;

  if (salesByAgentChart === null) {
    salesByAgentCtx = $(dest).get(0).getContext('2d');
  }
  const date = new Date();

  function fetchAndUpdateAgentMonthly() {
    let labelsList = [];
    let nums = [];

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

        const totalData = data.find((item) => item[0] === 'Total');
        const total = totalData ? totalData[1] : 0;
        const filteredData = data.filter((item) => item[0] !== 'Total');
        labelsList = filteredData.filter((item) => item[1] > 0).map((item) => item[0]);
        nums = filteredData.filter((item) => item[1] > 0).map((item) => item[1]);

        if (salesByAgentChart === null) {
          salesByAgentChart = new Chart(salesByAgentCtx, {
            type: chartType, // Assuming chartType is still 'bar'
            data: {
              labels: labelsList,
              datasets: [{
                data: nums,
                backgroundColor: '#2980B9', // Blue color
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
                  text: `${months[date.getMonth()]} Sales Analysis: total ${total}`,
                  color: '#fe9a43', // Darker blue color
                  position: 'bottom',
                  align: 'center',
                  font: {
                    weight: 'bold',
                    size: 12, // Adjust font size
                  },
                  padding: 5, // Adjust padding for spacing
                  fullSize: true,
                },
                legend: {
                  display: false,
                },
              },
              indexAxis: 'y', // Explicitly set y-axis as the index axis
              barPercentage: 0.7, // Adjust bar width
              categoryPercentage: 0.7, // Adjust spacing between bars
              scales: {
                x: {
                  grid: {
                    display: false, // Hide grid lines
                  },

                  ticks: {
                    beginAtZero: true, // Start axis at 0
                    stepSize: 1, // Show values for each agent
                    color: '#fe9a43', // Darker blue color
                    font: {
                      size: 9, // Adjust font size
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
                      size: 9, // Adjust font size
                      weight: 'bold', // Regular font weight
                    },
                  },
                },
              },
            },
          });
        } else {
          salesByAgentChart.data.labels = labelsList;
          salesByAgentChart.data.datasets[0].data = nums;
          salesByAgentChart.data.datasets[0].label = `${months[date.getMonth()]} Total Loan Sales: ${total}`;
          salesByAgentChart.update();
        }
        setTimeout(fetchAndUpdateAgentMonthly, 5 * 60 * 1000);
      },
      error(err) {
        console.error(err);
      },
    });
  }
  fetchAndUpdateAgentMonthly();
}

const dest_monthly = '.agent_sales_loan_chart';
const url_monthly = '/system_core_1/get_sale_by_agent_monthy_loan/';
const loader_monthly = '.agent_sales_loan_chart_loader';
const dest_monthly2 = '.agent_sales_cash_chart';
const url_monthly2 = '/system_core_1/get_sale_by_agent_monthy_cash/';
const loader_monthly2 = '.agent_sales_cash_chart_loader';

updateSalesByAgentChart(url_monthly, dest_monthly,
  'bar', loader_monthly);
updateSalesByAgentChart(url_monthly2, dest_monthly2, 'bar', loader_monthly2);
