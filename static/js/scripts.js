    $(document).ready(function() {
    

    // Checkout button handler
    $('#buy-item-button').click(async function() {
        try {
            const csrftoken = getCookie('csrftoken');
            const itemId = $(this).data('item-id');
            const response = await fetch(`/orders/buy/item/${itemId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({})
            });
            
            const session = await response.json();
            // Redirect to Stripe Checkout
            const result = await stripe.redirectToCheckout({ sessionId: session.session });
            
            if (result.error) {
                showToast(result.error.message);
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('An error occurred during checkout');
        }
    });
    // Update cart badge
    
    // Show toast notification
    function showToast(message) {
        const toast = `<div class="toast show position-fixed bottom-0 end-0 m-3" role="alert">
            <div class="toast-header">
                <strong class="me-auto">Notification</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>`;
        
        $('body').append(toast);
        setTimeout(() => $('.toast').remove(), 3000);
    }
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}