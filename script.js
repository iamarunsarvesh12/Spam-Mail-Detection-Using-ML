// Character Counter Logic
const textarea = document.getElementById('messageInput');
const currentCount = document.getElementById('currentCount');

textarea.addEventListener('input', function() {
    currentCount.textContent = this.value.length;
});

// Submit Logic
async function analyzeMessage() {
    const message = textarea.value;
    const btn = document.getElementById('analyzeBtn');
    const resultContainer = document.getElementById('resultContainer');
    const resultLabel = document.getElementById('resultLabel');
    const resultProb = document.getElementById('resultProb');
    const resultIcon = document.getElementById('resultIcon');

    if (!message.trim()) {
        alert("Please enter a message to analyze.");
        return;
    }

    // UI Loading state
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';
    resultContainer.classList.add('hidden');

    try {
        // Send request to Flask backend
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        if (response.ok) {
            // Remove old classes
            resultContainer.classList.remove('is-spam', 'not-spam');
            resultIcon.classList.remove('fa-triangle-exclamation', 'fa-circle-check');

            // Format probability to percentage
            const percentage = (data.spam_probability * 100).toFixed(2) + "%";

            // Update UI based on result
            if (data.label === "Spam") {
                resultContainer.classList.add('is-spam');
                resultIcon.classList.add('fa-triangle-exclamation');
            } else {
                resultContainer.classList.add('not-spam');
                resultIcon.classList.add('fa-circle-check');
            }

            resultLabel.textContent = `Result: ${data.label}`;
            resultProb.textContent = `Probability: ${percentage}`;
            resultContainer.classList.remove('hidden');
        } else {
            alert(data.error || "Something went wrong.");
        }
    } catch (error) {
        console.error('Error:', error);
        alert("Failed to connect to the server.");
    } finally {
        // Reset button
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-magnifying-glass"></i> Analyze Message';
    }
}