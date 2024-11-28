// Timer logic
document.addEventListener('DOMContentLoaded', () => {
    const timer = document.getElementById('timer');
    const startTime = new Date();

    function updateTimer() {
        const currentTime = new Date();
        const elapsedTime = currentTime - startTime;

        const seconds = Math.floor((elapsedTime / 1000) % 60);
        const minutes = Math.floor((elapsedTime / (1000 * 60)) % 60);
        const hours = Math.floor((elapsedTime / (1000 * 60 * 60)));

        timer.textContent = `${hours}h ${minutes}m ${seconds}s`;
    }

    setInterval(updateTimer, 1000);

    // AJAX logic for set completion
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        document.querySelectorAll('.set-completed-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', (event) => {
            const setId = event.target.dataset.setId;
            const isCompleted = event.target.checked;
            const url = event.target.dataset.url;  // Get the dynamic URL from the template

            console.log('Checkbox clicked:', { setId, isCompleted, url }); // Debugging log

            fetch(url, {  // Use dynamic URL here
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    set_id: setId,
                    is_completed: isCompleted
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Server response:', data); // Debugging log
            })
            .catch(error => {
                console.error('Error during fetch:', error);
            });
        });
    });
});
