$(document).ready(function() {
    // Function to fetch and display promoter data
    const input = $('#search_term');
    const form = $('form');
    const defualtFilter = $('#defualtfilter');

    function fetchPromoterData(page = 1, searchQuery = '') {
        const loader = $('#loader');
        $.ajax({
            url: '/system_core_1/promoters_data',
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
                renderPromoterCards(response.data_by_promoters);
                renderPagination(response.pagination);
            },
            error: function(xhr, status, error) {
                console.error("Error fetching data: ", error);
            }
        });
    }

    // Function to render promoter cards
    function renderPromoterCards(data) {
        const row = $('.container .row');
        row.empty(); // Clear existing content

        data.forEach(function(item) {
            const card = `
                <div class="col-md-4 col-sm-6 mb-4">
                    <div class="card common-bg rounded-start">
                        <div class="card-header text-center">
                            <h4 class="card-title fw-bold">${item.promoter.first_name} ${item.promoter.last_name}</h4>
                            <p class="card-text fw-bold">Phone No: ${item.promoter.phone_number}</p>
                        </div>
                        <a href="/system_core_1/devices_per_promoter/${item.promoter.id}">
                            <div class="card-body ${item.color_code}" style="padding: 5px;">
                                <p class="card-text"><strong class="text-info fw-bold">Total In Stock:</strong> <span>${item.total_devices}</span></p>
                                <p class="card-text"><strong class="text-info fw-bold">On-Time Devices:</strong> <span>${item.within_due_date}</span></p>
                                <p class="card-text"><strong class="text-info fw-bold">Overdue Devices:</strong> <span>${item.missed_due_date}</span></p>
                            </div>
                        </a>
                    </div>
                </div>
            `;
            row.append(card);
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
        const searchQuery = $('#search_term').val();
        fetchPromoterData(page, searchQuery);
    });

    // Handle search form submission
    input.on('input', function() {
        form.submit();
    });

    form.on('submit', function(event) {
        event.preventDefault();
        const searchQuery = input.val();
        fetchPromoterData(1, searchQuery);
    });

    // Initial fetch
    fetchPromoterData();
});
