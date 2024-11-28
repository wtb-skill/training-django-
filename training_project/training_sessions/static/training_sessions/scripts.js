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

            console.log('Checkbox clicked:', { setId, isCompleted }); // Debugging log

            fetch('/training-session/mark-set-completed/', {
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
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    console.log('Server response:', data); // Debugging log
                } else {
                    console.error('Server error:', data.error);
                    alert('There was an issue updating the set. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error during fetch:', error);
                alert('A network error occurred. Please check your connection and try again.');
            });
        });
    });
});
