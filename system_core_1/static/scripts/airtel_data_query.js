$(document).ready(function() {
    // Function to fetch and display Airtel devices data
    const input = $('#search_data');
    const form = $('form');
    const container = $('#container');
    const defualtFilter = $('#defualtfilter');
    const heading = $('#container_head');
    const loader = $('#loader');
    loader.show();

    const airtelDevicesTable = `<div class="table-responsive">
        <table class="table table-secondary table-hover table-bordered
        table-sm" id="airtelDevicesTable">
            <thead>
                <t class="common-bg">
                    <th scope="col">Promoter</th>
                    <th scope="col">Total Devices</th>
                    <th scope="col">In Stock</th>
                    <th scope="col" style="background-color: blue;">MIFI</th>
                    <th scope="col" style="background-color: purple;">IDU</th>
                    <th scope="col">Tody's Collection</th>
                    <th scope="col">Within due date</th>
                    <th scope="col">Overdue</th>
                    <th scope="col">Action</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        </table>
    </div>`;

    function fetchAirtelDevicesData(page = 1, searchQuery = '') {
        const loader = $('#loader');
        $.ajax({
            url: '/system_core_1/airtel_devices_data', // Update this URL to match your Django URL routing
            type: 'GET',
            data: {
                page: page,
                search_query: searchQuery
             },
            dataType: 'json',
            beforeSend() {
                loader.show();
            },
            success: function(response) {
                loader.hide();
                renderTable(response.data_by_promoters);
                renderPagination(response.pagination);
            },
            error: function(xhr, status, error) {
                console.error("Error fetching data: ", error);
            }
        });
    }

    // Function to render table rows
    function renderTable(data) {
        const tbody = $('#airtelDevicesTable tbody');
        tbody.empty(); // Clear existing table content

        data.forEach(function(item) {
            const row = `
                <tr>
                    <td style="background-color: ${item.bg};">${item.promoter.first_name} ${item.promoter.last_name}</td>
                    <td>${item.total_devices}</td>
                    <td>${item.total_devices}</td>
                    <td>${item.mifi}</td>
                    <td>${item.idu}</td>
                    <td>${item.todays_collection}</td>
                    <td>${item.within_due_date}</td>
                    <td style="background-color: ${item.bg};">${item.missed_due_date}</td>
                    <td>
                        <button class="btn btn-sm" data-bs-toggle="modal" data-bs-target="#Data${item.promoter.id}">
                            <span class="material-icons">send</span>
                        </button>
                    </td>
                </tr>
            `;
            tbody.append(row);
            $('body').append(
                `
                <div class="modal fade" id="Data${item.promoter.id}" tabindex="-1" aria-labelledby="Data${item.promoter.id}View" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title text-center fw-bold">Payment by ${item.promoter.first_name} ${item.promoter.last_name}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body common-bg">
                                <form action="/system_core_1/record_airtel_devices_payment/" method="post">
                                    <input type="hidden" name="promoter_id" value="${item.promoter.id}">
                                    <label for="id_mifi">How many MIFI devices paid</label>
                                    <input type="number" name="id_mifi" class="form-control">
                                    <br>
                                    <label for="id_router">How many IDU devices paid</label>
                                    <input type="number" name="id_idu" class="form-control">
                                    <br>
                                    <label for="Amount_paid">Amount paid</label>
                                    <input type="number" name="Amount_paid" class="form-control">
                                    <br>
                                    <div class="d-flex justify-content-center">
                                        <button type="submit" class="btn bg-secondary w-25">Send</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>`
            );

        });
    }

    // Function to render pagination
    function renderPagination(pagination) {
        const paginationContainer = $('.pagination .step-links');
        paginationContainer.empty(); // Clear existing pagination

        if (pagination.has_previous) {
            paginationContainer.append(`<a href="#" data-page="1" class="btn common-bg">first</a>`);
            paginationContainer.append(`<a href="#" data-page="${pagination.previous_page_number}" class="btn common-bg">previous</a>`);
        }

        paginationContainer.append(`<span class="current fs-5">Page ${pagination.current_page} of ${pagination.total_pages}</span>`);

        if (pagination.has_next) {
            paginationContainer.append(`<a href="#" data-page="${pagination.next_page_number}" class="btn common-bg">next</a>`);
            paginationContainer.append(`<a href="#" data-page="${pagination.num_pages}" class="btn common-bg">last</a>`);
        }
    }

    // Handle pagination clicks
    $(document).on('click', '.pagination a', function(event) {
        event.preventDefault();
        const page = $(this).data('page');
        fetchAirtelDevicesData(page);
    });

    // Handle search form submission
    input.on('input', function() {
        form.submit();
    });

    form.on('submit', function(event) {
        event.preventDefault();
        const searchQuery = input.val();
        fetchAirtelDevicesData(1, searchQuery);
    });

    // Handle reset button click
    defualtFilter.on('click', function(event) {
        input.val('');
        container.empty();
        container.append(airtelDevicesTable);
        fetchAirtelDevicesData();
    });

    // Initial fetch
    fetchAirtelDevicesData();
});
