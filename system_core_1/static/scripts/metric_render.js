export default function metricsRender() {
    const container = $('#container');
    const chartsContainer = `
        <section class="charts_by_chartjs">
            <div class="row gy-3">
                <div class="col-md-6 col-12">
                    <div class="card bg-dark">
                        <div class="card-header text-center">
                            <h4 class="text-muted fw-bold">Daily Devices collected</h4>
                        </div>
                        <div class="card-body">
                            <canvas class="dailyCollectionsChart" width="300" height="300"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-12">
                    <div class="card bg-dark">
                        <div class="card-header text-center">
                            <h4 class="fw-bold text-muted">Available Stock</h4>
                        </div>
                        <div class="card-body">
                            <canvas class="available_stock_chart" width="300" height="300"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <br>
        <section class="charts_by_chartjs">
            <div class="row gy-3">
                <div class="col-md-6 col-12">
                    <div class="card bg-dark">
                        <div class="card-header text-center">
                            <h4 class="fw-bold text-muted">Daily Payments</h4>
                        </div>
                        <div class="card-body">
                            <div class="weekly_sales_loader_loan"></div>
                            <canvas class="Weekly_sales_chart_loan" width="300" height="300"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-12">
                    <div class="card bg-dark">
                        <div class="card-header text-center">
                            <h4 class="fw-bold text-muted">Stock By Individuals</h4>
                        </div>
                        <div class="card-body">
                            <div class="weekly_sales_loader_cash"></div>
                            <canvas class="Weekly_sales_chart_cash" width="300" height="300"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <br>
        <section class="charts_by_chartjs">
            <div class="row gy-3">
                <div class="col-md-6 col-12">
                    <div class="card bg-dark">
                        <div class="card-header text-center">
                            <h4 class="fw-bold text-muted">Overdue Stock</h4>
                        </div>
                        <div class="card-body">
                            <div class="agent_sales_loan_chart_loader"></div>
                            <canvas class="agent_sales_loan_chart" width="400" height="400"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-12">
                    <div class="card bg-dark">
                        <div class="card-header text-center">
                            <h4 class="fw-bold text-muted">Monthly Sales</h4>
                        </div>
                        <div class="card-body">
                            <div class="agent_sales_cash_chart_loader"></div>
                            <canvas class="agent_sales_cash_chart" width="400" height="400"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <br>
        <section class="charts_by_chartjs">
            <div class="row gy-3">
                <div class="col-md-6 col-12">
                    <div class="card bg-dark">
                        <div class="card-header text-center">
                            <h4 class="fw-bold text-muted">Agent Overall Stock</h4>
                        </div>
                        <div class="card-body">
                            <div class="loading-message-stock"></div>
                            <canvas class="all_agents_stock_chart" width="400" height="400"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-12">
                    <div class="card bg-dark">
                        <div class="card-header text-center">
                            <h4 class="fw-bold text-muted">Main Shop Stock</h4>
                        </div>
                        <div class="card-body">
                            <div class="loading-message-shop"></div>
                            <canvas class="main_stock_chart" width="400" height="400"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    `;
    container.html(chartsContainer);
}