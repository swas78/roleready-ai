document.addEventListener('DOMContentLoaded', () => {

    const setupDropZone = (dropId, inputId) => {
        const dropZone = document.getElementById(dropId);
        const input = document.getElementById(inputId);
        const info = dropZone.querySelector('.file-info');

        dropZone.addEventListener('click', () => input.click());
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults (e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
        });

        dropZone.addEventListener('drop', (e) => {
            let dt = e.dataTransfer;
            let files = dt.files;
            input.files = files;
            updateInfo(files[0]);
        });

        input.addEventListener('change', (e) => {
            if (e.target.files.length) updateInfo(e.target.files[0]);
        });

        function updateInfo(file) {
            if(file) info.textContent = file.name;
        }
    }

    setupDropZone('resume-drop', 'resume-input');
    setupDropZone('jd-drop', 'jd-input');

    const personaCards = document.querySelectorAll('.persona-card');
    const demoInput = document.getElementById('demo-input');
    
    personaCards.forEach(card => {
        card.addEventListener('click', () => {
            personaCards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            demoInput.value = card.getAttribute('data-key');
        });
    });

    const form = document.getElementById('analyze-form');
    const submitBtn = document.getElementById('submit-btn');

    form.addEventListener('submit', () => {
        submitBtn.classList.add('loading');
    });
});
