$(document).ready(function () {
    const loader = $('#loader');

    const fetchData = () => {
        $.ajax({
            url: '/system_core_1/revenue_by_category/',
            method: 'GET',
            contentType: 'application/json',
            beforeSend() {
                $('#loader').show();
            },
            success(data) {
                $('#loader').hide();
            },
        });
    }

    fetchData();
});

// function revCostByCategory(data) {
//     let revCostByCategoryChart = null;
//     let revCostByCategoryctx = null;

//     if (revCostByCategoryChart === null) {
//         revCostByCategoryctx = $('.revCostByCategoryChart').get(0).getContext('2d');
//     }

//     const date = new Date();

//     function fetchAndUpdateDailyData() {
//         const modelList = [
//             "Both Price & Cost",
//             "Cost Only",
//             "Price Only",
//             "No Price or Cost",
//         ];
//         const values = [
//             data.both_price_and_cost,
//             data.cost_only,
//             data.price_only,
//             data.no_price_or_cost,
//         ]

//         if (revCostByCategoryChart === null) {
//             revCostByCategoryChart = new Chart(revCostByCategoryctx, {
//                 type: 'doughnut',
//                 data: {
//                     labels: modelList,
//                     datasets: [],
//                 },
//                 options: {
//                     responsive: true,
//                     maintainAspectRatio: false,
//                     plugins: {
//                         title: {
//                             display: true,
//                             text: 'Revenue and Cost by Category',
//                         },
//                     },
//                 },
//             });
//         } else {
//             revCostByCategoryChart.data.labels = modelList;
//             revCostByCategoryChart.data.datasets[0].data = values;
//             revCostByCategoryChart.update();
//         }
//     }

//     fetchAndUpdateDailyData();
// }