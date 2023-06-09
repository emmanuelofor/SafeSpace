document.addEventListener("DOMContentLoaded", function() {

    // Find the send message button in the document
    const sendMessageButton = document.querySelector('.contact-form .btn');

    // Listen for a click event on the send message button
    sendMessageButton.addEventListener('click', function(event) {
        
        // Prevent the default action of the click event (like navigating to another page)
        event.preventDefault();
        
        // Display the thank you message
        alert('Thank you for contacting us. We will get back to you soon');
        
    });

});
