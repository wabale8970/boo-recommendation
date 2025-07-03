// Book Recommendation System - Main JavaScript File

// Enable Bootstrap tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.classList.add('fade-in');
    });
});

// Function to handle "Show More" button for book descriptions
function toggleDescription(bookId) {
    const shortDesc = document.getElementById(`short-desc-${bookId}`);
    const fullDesc = document.getElementById(`full-desc-${bookId}`);
    const toggleBtn = document.getElementById(`toggle-desc-${bookId}`);
    
    if (shortDesc.style.display !== 'none') {
        shortDesc.style.display = 'none';
        fullDesc.style.display = 'block';
        toggleBtn.textContent = 'Show Less';
    } else {
        shortDesc.style.display = 'block';
        fullDesc.style.display = 'none';
        toggleBtn.textContent = 'Show More';
    }
}

// Confirm before removing a book from favorites
function confirmRemove(event, bookTitle) {
    if (!confirm(`Are you sure you want to remove "${bookTitle}" from your favorites?`)) {
        event.preventDefault();
    }
} 