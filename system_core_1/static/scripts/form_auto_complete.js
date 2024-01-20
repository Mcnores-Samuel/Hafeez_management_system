$(document).ready(function() {
    // field to listen on change and search
    const name = $('#id_name');
    const phone_type = $('#id_phone_type');
    const category = $('#id_category');
    const spec = $('#id_spec');
    const screen_size = $('#id_screen_size');
    const os = $('#id_os');
    const battery = $('#id_battery');
    const camera = $('#id_camera');

    name.on('change', function() {
        const url = "/system_core_1/autocomplete/" + name.val() + "/";

        $.ajax({
            url: url,
            method: "GET",
            contentType: "application/json",

            success: function(data) {
                console.log(data);

                // append the new results
                $.each(data, function(key, value) {
                    if (key == 'name') {
                        name.val(value);
                    }
                    if (key == 'phone_type') {
                        phone_type.val(value);
                    }
                    if (key == 'category') {
                        category.val(value);
                    }
                    if (key == 'spec') {
                        spec.val(value);
                    }
                    if (key == 'screen_size') {
                        screen_size.val(value);
                    }
                    if (key == 'os') {
                        os.val(value);
                    }
                    if (key == 'battery') {
                        battery.val(value);
                    }
                    if (key == 'camera') {
                        camera.val(value);
                    }
                });
            },

        });
    });
});