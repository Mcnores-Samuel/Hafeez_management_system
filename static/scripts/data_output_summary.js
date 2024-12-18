function renderTable(data, targetElement) {
    targetElement.html('');

    if (data.length === 0) {
        targetElement.append(`
            <tr>
                <td colspan="2" class="text-center text-danger">No data available</td>
            </tr>
        `);
        return;
    }

    $.each(data, function (model, value) {
        targetElement.append(`
            <tr>
                <td>${model}</td>
                <td>${value}</td>
            </tr>
        `);
    });
}

function formatDate(date) {
    const d = new Date(date);
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return d.toLocaleString(undefined, options);
}

function stockTable(data, targetElement) {
    const table = $('<table class="table table-bordered table-striped table-dark"></table>');
    const thead = $('<thead style="position: sticky; top: -1px; background-color: azure;"></thead>');
    const tbody = $('<tbody></tbody>');

    const h1 = $('<h1 class="text-center bg-info w-100">Stock details</h1>');



    thead.append(`
        <tr>
            <th>Category</th>
            <th>Model</th>
            <th>IMEI</th>
            <th>Date Collected</th>
            <th>Action</th>
        <tr>
    `);

    $.each(data, function (index, item) {
        tbody.append(`
            <tr>
                <td>${item.category}</td>
                <td>${item.phone_type}</td>
                <td>${item.imei}</td>
                <td>${formatDate(item.date_collected)}</td>
                <td>
                    <form action="/system_core_1/data_search/" method="post" class="d-flex w-100">
                        <input type="search" class="form-control me-2" name="search_query" id="search" value="${item.imei}" hidden>
                        <button class="btn btn-outline-success" type="submit"><span class="material-icons">search</span></button>
                    </form>
                </td>
            </tr>
        `);
    });

    targetElement.append(h1);
    table.append(thead);
    table.append(tbody);
    targetElement.append(table);
}

export { renderTable, stockTable  };