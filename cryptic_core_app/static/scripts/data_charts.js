const months = [
  'January', 'February',
  'March', 'April', 'May',
  'June', 'July', 'August',
  'September', 'October',
  'November', 'December'
];

let monthly_ctx = null;
let monthly_chart = null;
let weekly_sales_chart = null;
let weekly_ctx = null;
let daily_sales_chart = null;
let daily_ctx = null;

function update_monthly_Chart () {
  if (monthly_chart === null) {
    monthly_ctx = document.querySelector('.products').getContext('2d');
  }

  const date = new Date();
  const labels_list = [];
  const nums = [];
  let chart_type = 'line';

  fetch('/get_models_json/')
    .then(response => response.json())
    .then(data => {
      for (let i = 0; i < data.length; i++) {
        if (data.length > 20) {
          chart_type = 'line';
        }
        labels_list.push(data[i].type);
        nums.push(data[i].total);
      }

      if (monthly_chart === null) {
        monthly_chart = new Chart(monthly_ctx, {
          type: chart_type,
          data: {
            labels: labels_list,
            datasets: [{
              label: months[date.getMonth()] + ' Data',
              data: nums,
              backgroundColor: ['#000C66', 'blue', 'green', 'yellow', 'gray'],
              borderColor: ['#000C66', 'blue', 'green', 'yellow', 'gray'],
              borderWidth: 2
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            events: ['mousemove'],
            interaction: {
              mode: 'nearest'
            },
            plugins: {
              title: {
                display: true,
                text: 'Monthy Inventory Analysis',
                color: 'navy',
                position: 'bottom',
                align: 'center',
                font: {
                  weight: 'bold'
                },
                padding: 8,
                fullSize: true
              }
            }
          }
        });
      } else {
        monthly_chart.data.labels = labels_list;
        monthly_chart.data.datasets[0].data = nums;
        monthly_chart.update();
      }
    })
    .catch(err => console.error(err));
}

function update_daily_Chart () {
  if (daily_sales_chart === null) {
    daily_ctx = document.querySelector('.daily_sales_chart').getContext('2d');
  }

  const date = new Date();
  const model_list = [];
  const total = [];
  const chart_type = 'line';

  fetch('/daily_entries_json/')
    .then(response => response.json())
    .then(data => {
      for (let i = 0; i < data.length; i++) {
        model_list.push(data[i].type);
        total.push(data[i].total);
      }

      if (daily_sales_chart === null) {
        daily_sales_chart = new Chart(daily_ctx, {
          type: chart_type,
          data: {
            labels: model_list,
            datasets: [{
              label: date.toDateString(),
              data: total,
              backgroundColor: ['#877B89', 'blue', 'green', 'yellow', 'gray'],
              borderColor: ['#877B89', 'blue', 'green', 'yellow', 'gray'],
              borderWidth: 2
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            events: ['mousemove'],
            interaction: {
              mode: 'nearest'
            },
            plugins: {
              title: {
                display: true,
                text: 'Daily Sales Analysis',
                color: 'navy',
                position: 'bottom',
                align: 'center',
                font: {
                  weight: 'bold'
                },
                padding: 8,
                fullSize: true
              }
            }
          }
        });
      } else {
        daily_sales_chart.data.labels = labels_list;
        daily_sales_chart.data.datasets[0].data = nums;
        daily_sales_chart.update();
      }
    })
    .catch(err => console.error(err));
}

function update_weekly_Chart () {
  if (weekly_sales_chart === null) {
    weekly_ctx = document.querySelector('.Weekly_sales_chart').getContext('2d');
  }
  const labels_list = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
  const nums = [];
  let count = 0;
  const chart_type = 'line';

  fetch('/get_weekly_sales_json/')
    .then(response => response.json())
    .then(data => {
      for (const dayData of data) {
        for (const dayName in dayData) {
          if (dayData.hasOwnProperty(dayName)) {
            const items = dayData[dayName];
            for (const item of items) {
              count++;
            }
            nums.push(count);
          }
          count = 0;
        }
      }
      if (weekly_sales_chart === null) {
        weekly_sales_chart = new Chart(weekly_ctx, {
          type: chart_type,
          data: {
            labels: labels_list,
            datasets: [{
              label: 'This week',
              data: nums,
              backgroundColor: ['brown'],
              borderColor: ['rgb(47, 79, 79, 0.7)'],
              borderWidth: 2
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            events: ['mousemove'],
            interaction: {
              mode: 'nearest'
            },
            plugins: {
              title: {
                display: true,
                text: 'Weekly Sales Analysis',
                color: 'navy',
                position: 'bottom',
                align: 'center',
                font: {
                  weight: 'bold'
                },
                padding: 8,
                fullSize: true
              }
            }
          }
        });
      } else {
        weekly_sales_chart.data.labels = labels_list;
        weekly_sales_chart.data.datasets[0].data = nums;
        weekly_sales_chart.update();
      }
    })
    .catch(err => console.error(err));
}

document.addEventListener('DOMContentLoaded', function () {
  update_monthly_Chart();
  update_weekly_Chart();
  update_daily_Chart();
  setInterval(update_monthly_Chart, 10 * 60 * 1000);
  setInterval(update_weekly_Chart, 10 * 60 * 1000);
  setInterval(update_daily_Chart, 10 * 60 * 1000);
});
