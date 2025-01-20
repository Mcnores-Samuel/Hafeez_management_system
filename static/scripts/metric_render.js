export default function metricsRender() {
    const container = $('#container');
    const chartsContainer = `
        <section class="charts_by_chartjs">
            <div class="row gy-3">
                <div class="col-md-6 col-12">
                    <div class="card">
                        <div class="card-header text-center">
                            <h4 class="text-muted fw-bold">Daily Devices collected</h4>
                        </div>
                        <div class="card-body">
                            <canvas class="dailyCollectionsChart" width="300" height="300"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-12">
                    <div class="card">
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
                    <div class="card">
                        <div class="card-header text-center">
                            <h4 class="fw-bold text-muted">Daily Payments</h4>
                        </div>
                        <div class="card-body">
                            <canvas class="dailyPaymentsChart" width="300" height="300"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-12">
                    <div class="card">
                        <div class="card-header text-center">
                            <h4 class="fw-bold text-muted">Stock By Individuals</h4>
                        </div>
                        <div class="card-body">
                            <canvas class="stockByIndividualsChart" width="300" height="300"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <br>
        <section class="charts_by_chartjs">
            <div class="row gy-3">
                <div class="col-md-6 col-12">
                    <div class="card bg-danger">
                        <div class="card-header text-center">
                            <h4 class="fw-bold">Overdue Stock</h4>
                        </div>
                        <div class="card-body">
                            <canvas class="overdueStockChart" width="300" height="300"></canvas>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-12">
                    <div class="card bg-success">
                        <div class="card-header text-center">
                            <h4 class="fw-bold">Monthly Sales</h4>
                        </div>
                        <div class="card-body">
                            <canvas class="monthlySalesChart" width="300" height="300"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <br>
    `;
    container.html(chartsContainer);
}