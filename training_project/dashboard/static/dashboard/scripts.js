document.addEventListener('DOMContentLoaded', function() {
    const editLink = document.getElementById('edit-training-link');
    const editOptions = document.getElementById('edit-options');

    editLink.addEventListener('click', function() {
        editOptions.classList.toggle('hidden');
    });
});
