document.addEventListener("DOMContentLoaded", function() {
        // Get all the "Add Set" buttons
        var addSetButtons = document.querySelectorAll(".add-set-btn");

        // Add click event listener to each button
        addSetButtons.forEach(function(button) {
            button.addEventListener("click", function() {
                var exerciseOrderId = button.getAttribute("data-exercise-order-id");
                var formContainer = document.getElementById("add-set-form-" + exerciseOrderId);

                // Toggle the display of the form
                if (formContainer.style.display === "none") {
                    formContainer.style.display = "block";
                } else {
                    formContainer.style.display = "none";
                }
            });
        });
    });