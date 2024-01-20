$(document).ready(function() {
    // field to listen on change and search
    const name = $('#id_name');

    name.on('change', function() {
        const url = "/system_core_1/autocomplete/?name=" + name.val();

        $.ajax({
            url: url,
            method: "GET",
            contentType: "application/json",

            success: function(data) {
                console.log(data);
            },

        });
    });
});