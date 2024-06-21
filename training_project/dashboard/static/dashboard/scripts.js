document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript is loaded and running'); // Debugging statement
    const editLink = document.getElementById('edit-training-link');
    const editOptions = document.getElementById('edit-options');
    const startTrainingLink = document.getElementById('start-training-link');
    const trainingTemplatesContainer = document.getElementById('training-templates');

    editLink.addEventListener('click', function() {
        editOptions.classList.toggle('hidden');
    });

    startTrainingLink.addEventListener('click', function() {
        console.log('Start Training link clicked'); // Debugging statement
        fetch('/api/training-templates/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                console.log('Fetched data:', data); // Debugging statement
                trainingTemplatesContainer.innerHTML = '';
                data.templates.forEach(template => {
                    const templateLink = document.createElement('a');
                    templateLink.href = `/start-training/${template.id}`;
                    templateLink.textContent = template.name;
                    trainingTemplatesContainer.appendChild(templateLink);
                });
                trainingTemplatesContainer.classList.toggle('hidden');
            })
            .catch(error => console.error('Error fetching templates:', error));
    });
        // Close submenus if clicked outside
    document.addEventListener('click', function(event) {
        if (!editLink.contains(event.target) && !editOptions.contains(event.target)) {
            editOptions.classList.add('hidden'); // Hide edit options
        }
        if (!startTrainingLink.contains(event.target) && !trainingTemplatesContainer.contains(event.target)) {
            trainingTemplatesContainer.classList.add('hidden'); // Hide training templates
        }
    });
});
