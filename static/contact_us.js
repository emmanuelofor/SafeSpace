document.addEventListener("DOMContentLoaded", function() {

    // Find the form in the document
    const form = document.querySelector('.contact-form');

    // Listen for a submit event on the form
    form.addEventListener('submit', function(event) {
        
        // Check if all fields are filled
        const inputs = form.querySelectorAll('input, textarea');
        let allFilled = true;

        inputs.forEach(input => {
            if (input.value.trim() === '') {
                allFilled = false;
            }
        });

        if (!allFilled) {
            // Prevent the form from being submitted if any field is not filled
            event.preventDefault();
            
            // Optionally show an alert or some other form of message
            alert('Please fill all fields before submitting');
        } else {
            // Display the thank you message
            alert('Thank you for contacting us. We will get back to you soon');
        }
        
    });

});

