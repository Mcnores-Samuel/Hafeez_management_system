document.addEventListener("DOMContentLoaded", function() {
    // Get a reference to the "Phone type" select element
    const phoneTypeSelect = document.getElementById("id_phone_type");

    // Add an event listener to the "Phone type" select element
    phoneTypeSelect.addEventListener("change", function() {
        const phoneTypeValue = phoneTypeSelect.value;

        if (phoneTypeValue) {
            // Make an AJAX request to fetch data
            const xhr = new XMLHttpRequest();
            xhr.open("GET", "/get_item_data/?phone_type_id=" + phoneTypeValue, true);

            xhr.onload = function() {
                if (xhr.status === 200) {
                    try {
                        const data = JSON.parse(xhr.responseText);
                        // Populate the fields with the retrieved data
                        document.getElementById("id_name").value = data.name;
                        document.getElementById("id_category").value = data.category;
                        document.getElementById("id_spec").value = data.spec;
                        // Add similar lines for other fields
                    } catch (error) {
                        console.error("Error parsing JSON:", error);
                    }
                } else {
                    console.error("Request failed with status:", xhr.status);
                }
            };

            xhr.send();
        }
    });
});
