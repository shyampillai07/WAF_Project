document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript loaded successfully!");

    const form = document.getElementById("waf-form");
    const inputField = document.getElementById("user-input");
    const resultBox = document.getElementById("result-box");
    const resultMessage = document.getElementById("result-message");
    const submitBtn = document.getElementById("submit-btn");
    const loader = document.getElementById("loader");

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        console.log("Form submitted!");
        checkInput();
    });

    function checkInput() {
        const userInput = inputField.value.trim();
        console.log("User Input:", userInput);

        if (userInput === "") {
            showAlert("Please enter input!", "warning");
            return;
        }

        // Show loader and disable button
        loader.style.display = "block";
        submitBtn.disabled = true;

        fetch(`/check?input=${encodeURIComponent(userInput)}`)
    .then(response => response.json())
    .then(data => {
        loader.style.display = "none";
        submitBtn.disabled = false;
        console.log("Server Response:", data);

        // Check if data.message exists before accessing it
        if (data.message && data.message.toLowerCase().includes("safe")) {
            showAlert(data.message, "success");
        } else if (data.error) {
            showAlert(data.error, "danger"); // Display error message
        } else {
            showAlert("Unexpected response from the server.", "danger");
        }
    })
    .catch(error => {
        console.error("Fetch Error:", error);
        loader.style.display = "none";
        submitBtn.disabled = false;
        showAlert("An error occurred. Try again!", "danger");
    });
    }
    function showAlert(message, type) {
        console.log("Displaying Alert:", message, "Type:", type);
        
        const resultMessage = document.getElementById("result-message");
        resultMessage.className = `alert alert-${type}`; // Set alert class based on type
        resultMessage.innerHTML = message; // Set the alert message
        resultMessage.style.display = "block"; // Show the alert
    
        // Set timeout to hide alert after 15 seconds
        setTimeout(() => {
            resultMessage.style.display = "none";  
        }, 15000);
    }
});