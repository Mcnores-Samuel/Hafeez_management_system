/**
 * @name adminStockAnalysis - Function to update the stock analysis of the admin dashboard
 * @param {None} - None
 */
function adminStockAnalysis() {
  const overallStock = $('#overall_stock_analysis');
  const overallSales = $('#overall_sales_analysis');
  const mainShopSales = $('#main_shop_sales_analysis');
  const mainShopStock = $('#main_shop_stock_analysis');
  const progress = $('.progress-bar');
  const target = $('.text-end');

  function updateStockAnalysis() {
    $.ajax({
      url: '/system_core_1/admin_stock_analysis',
      type: 'GET',
      dataType: 'json',
      beforeSend() {
        overallStock.html(
          '<div class="spinner-border common-color spinner-border-sm" role="status"><span class="visually-hidden">Loading...</span></div>'
        );
        overallSales.html( '<div class="spinner-border common-color spinner-border-sm" role="status"><span class="visually-hidden">Loading...</span></div>');
        mainShopSales.html('<div class="spinner-border common-color spinner-border-sm" role="status"><span class="visually-hidden">Loading...</span></div>');
        target.html('<div class="spinner-border common-color spinner-border-sm" role="status"><span class="visually-hidden">Loading...</span></div>');
        mainShopStock.html('<div class="spinner-border common-color spinner-border-sm" role="status"><span class="visually-hidden">Loading...</span></div>');
        progress.css('width', '100%');
        progress.html('0%');
      },
      success(data) {
        overallStock.html(`${data.overall_stock} Devices`);
        overallSales.html(`${data.overall_sales} Devices`);
        mainShopSales.html(`${data.sales} Devices`);
        mainShopStock.html(`${data.main_shop_stock} Devices`);
        target.html(`${data.target} Devices`);
        if (data.progress < 50) {
          progress.css('background-color', 'red');
        }
        if (data.progress >= 50 && data.progress < 75) {
          progress.css('background-color', 'blue');
        }
        if (data.progress >= 75) {
          progress.css('background-color', 'purple');
        }
        progress.css('width', `${data.progress}%`);
        progress.html(`${data.progress}%`);
      },
    });
  }
  setTimeout(updateStockAnalysis, 3000);
}

function formatRevenue(value) {
  if (value >= 1000000) {
    return (value / 1000000).toFixed(3) + 'M';
  } else if (value >= 1000) {
    return (value / 1000).toFixed(2) + 'K';
  } else {
    return Number(value).toFixed(2);
  }
}

function costaAndRevenueAnalysis() {

  const estimatedCost = $('#estimated-cost');
  const estimatedRevenue = $('#estimated-revenue');

  $.ajax({
    url: '/system_core_1/getCostAndRevenue/',
    method: 'GET',
    contentType: 'application/json',
    beforeSend() {
      estimatedCost.html('<div class="spinner-border text-success spinner-border-sm" role="status"><span class="visually-hidden">Loading...</span></div>');
      estimatedRevenue.html('<div class="spinner-border text-primary spinner-border-sm" role="status"><span class="visually-hidden">Loading...</span></div>');
    },
    success(data) {
      estimatedCost.html(`MWK ${formatRevenue(data.total_cost)}`);
      estimatedRevenue.html(`MWK ${formatRevenue(data.total_revenue)}`);
    },
  });
}

$(document).ready(() => {
  adminStockAnalysis();
  costaAndRevenueAnalysis();
});
