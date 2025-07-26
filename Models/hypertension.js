document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('hypertensionForm');
    const resultSection = document.getElementById('result');
    const resultMessage = document.getElementById('resultMessage');
    const probabilityDisplay = document.getElementById('probability');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            age: parseFloat(form.age.value),
            salt_intake: parseFloat(form.salt_intake.value),
            stress_score: parseFloat(form.stress_score.value),
            sleep_duration: parseFloat(form.sleep_duration.value),
            bmi: parseFloat(form.bmi.value),
            family_history: form.family_history.value,
            smoking_status: form.smoking_status.value
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (data.error) throw new Error(data.error);
            
            resultMessage.textContent = data.message;
            probabilityDisplay.textContent = `Risk percentage: ${data.risk_percent}%`;
            
            // Style based on risk
            resultSection.style.backgroundColor = data.prediction ? '#ffebee' : '#e8f5e9';
            resultMessage.style.color = data.prediction ? '#c62828' : '#2e7d32';
            
            form.classList.add('hidden');
            resultSection.classList.remove('hidden');
            
        } catch (error) {
            resultMessage.textContent = `Error: ${error.message}`;
            resultMessage.style.color = '#c62828';
            resultSection.classList.remove('hidden');
        }
    });

    document.getElementById('resetBtn').addEventListener('click', () => {
        form.reset();
        resultSection.classList.add('hidden');
        form.classList.remove('hidden');
    });
});