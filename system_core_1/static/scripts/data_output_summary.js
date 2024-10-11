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



    thead.append(`
        <tr>
            <th>Category</th>
            <th>Model</th>
            <th>IMEI</th>
            <th>Date Collected</th>
        <tr>
    `);

    $.each(data, function (index, item) {
        tbody.append(`
            <tr>
                <td>${item.category}</td>
                <td>${item.phone_type}</td>
                <td>${item.imei}</td>
                <td>${formatDate(item.date_collected)}</td>
            </tr>
        `);
    });

    table.append(thead);
    table.append(tbody);
    targetElement.append(table);
}

export { renderTable, stockTable  };