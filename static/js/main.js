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

                if (data.message.toLowerCase().includes("safe")) {
                    showAlert(data.message,"success");
                } else {
                    showAlert(data.message, "danger");
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
    
        const resultBox = document.getElementById("result-box");
        resultBox.style.display = "block";  // Ensure it's visible
    
        resultBox.innerHTML = `
            <div class="alert alert-${type}" role="alert">
                ${message}
            </div>
        `;
    
        // Set timeout to 15 seconds instead of 5
        setTimeout(() => {
            resultBox.style.display = "none";  
        }, 15000);
    }
});