document.addEventListener('DOMContentLoaded', function () {
    // --- Star Rating Functionality ---
    const starRatingContainer = document.querySelector('.star-rating');
    if (starRatingContainer) {
        const stars = starRatingContainer.querySelectorAll('input[type="radio"]');
        stars.forEach(star => {
            star.addEventListener('change', function () {
                const movieId = starRatingContainer.dataset.movieId;
                const rating = this.value;

                // Send the rating to the server
                submitRating(movieId, rating);
            });
        });
    }

    // --- Add to Watchlist Functionality ---
    const watchlistButtons = document.querySelectorAll('.add-to-watchlist');
    watchlistButtons.forEach(button => {
        button.addEventListener('click', function () {
            const movieId = this.dataset.movieId;
            addToWatchlist(movieId);
        });
    });

    // --- Helper function to show notifications ---
    function showToast(title, message) {
        const toastEl = document.getElementById('notificationToast');
        const toastTitle = document.getElementById('toast-title');
        const toastBody = document.getElementById('toast-body');

        toastTitle.textContent = title;
        toastBody.textContent = message;

        const toast = new bootstrap.Toast(toastEl);
        toast.show();
    }

    // --- API Call Functions ---

    // Function to submit a rating via Fetch API
    async function submitRating(movieId, rating) {
        const formData = new FormData();
        formData.append('rating', rating);

        try {
            const response = await fetch(`/rate/${movieId}`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            showToast('Rating Submitted', data.message);

            // Update the average rating on the page
            const avgRatingEl = document.getElementById('avg-rating');
            if (avgRatingEl) {
                avgRatingEl.textContent = data.new_avg_rating;
            }
        } catch (error) {
            console.error('Error submitting rating:', error);
            showToast('Error', 'Could not submit rating. Please try again.');
        }
    }

    // Function to add a movie to the watchlist via Fetch API
    async function addToWatchlist(movieId) {
        try {
            const response = await fetch(`/watchlist/add/${movieId}`, {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            let title = 'Watchlist';
            if(data.action === 'added') title = 'Success';
            if(data.action === 'exists') title = 'Info';
            
            showToast(title, data.message);

        } catch (error) {
            console.error('Error adding to watchlist:', error);
            showToast('Error', 'Could not add to watchlist. Please try again.');
        }
    }
});