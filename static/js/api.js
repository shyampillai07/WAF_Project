async function checkSecurity(input) {
    const resultDiv = document.getElementById("result");
    
    try {
        const response = await fetch(`/check?input=${encodeURIComponent(input)}`);
        const data = await response.json();
        
        if (data.error) {
            resultDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        } else {
            resultDiv.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
        }
    } catch (error) {
        console.error("Error:", error);
        resultDiv.innerHTML = `<div class="alert alert-warning">An error occurred.</div>`;
    }
}