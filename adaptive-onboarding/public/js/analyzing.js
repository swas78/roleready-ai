document.addEventListener('DOMContentLoaded', () => {
    const steps = document.querySelectorAll('.step-row');
    const statusEl = document.querySelector('.status-text');
    const errorWrap = document.querySelector('.analyze-error');
    const errorMsg = document.querySelector('.error-msg');
    const pipeline = document.querySelector('.pipeline');

    const statusMessages = [
        "Warming up LLaMA 3...",
        "Evaluating candidate claims against required profile...",
        "Mapping semantic distances dynamically...",
        "Synthesizing cosine similarity thresholds...",
        "Building acyclic directed graphs...",
        "Validating topological constraints..."
    ];

    let currentStep = 1;
    let animInterval;

    function activateStep(index) {
        if (index > 0 && index <= 5) {
            steps[index - 1].classList.remove('active');
            steps[index - 1].classList.add('done');
        }
        if (index <= 5) {
            steps[index].classList.add('active');
            steps[index].classList.remove('done');
            statusEl.textContent = statusMessages[index];
            statusEl.style.opacity = 0;
            setTimeout(() => { statusEl.style.opacity = 1; }, 50); // slight fade
        }
    }

    function completeStep(index) {
        if (steps[index]) {
            steps[index].classList.remove('active');
            steps[index].classList.add('done');
        }
    }

    function showError(message) {
        pipeline.style.display = 'none';
        statusEl.style.display = 'none';
        errorWrap.style.display = 'block';
        errorMsg.textContent = message;
        clearInterval(animInterval);
    }

    async function callBackend() {
        try {
            const res = await fetch('/analyzing/run');
            const data = await res.json();
            
            if (!res.ok || !data.ok) {
                showError(data.error || 'Unknown server error fetching analysis result.');
                return;
            }
            
            clearInterval(animInterval);
            
            // Fast forward through remaining steps visually
            for(let i = currentStep; i <= 5; i++) {
                completeStep(i);
            }
            statusEl.textContent = "Analysis Complete! Assembling Dashboard...";
            
            setTimeout(() => {
                window.location.href = '/results';
            }, 400);

        } catch (err) {
            showError(err.message);
        }
    }

    // Start faux-animation
    activateStep(1);
    animInterval = setInterval(() => {
        if (currentStep < 4) {
            currentStep++;
            activateStep(currentStep);
        }
    }, 700);

    // Hit the endpoint immediately
    callBackend();
});
