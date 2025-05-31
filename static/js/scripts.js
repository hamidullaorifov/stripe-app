$(document).ready(function() {

    // Checkout button handler
    async function initiateStripeCheckout(url)
    {
        try {
            const csrftoken = getCookie('csrftoken');
            const response = await fetch(url, {
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
    }
    async function handleStripePayment(url, buttonId) {
        const response = await fetch(url);
        const data = await response.json();
        const { clientSecret } = data
        const elements = stripe.elements( {clientSecret} );
        const paymentElement = elements.create('payment');
        paymentElement.mount('#payment-element');
        
        document.getElementById('payment-element').style.display = 'block';
        const button = document.getElementById(buttonId);
        button.style.display = 'none';
        
        const confirmButton = document.createElement('button');
        confirmButton.textContent = 'Confirm Payment';
        confirmButton.className = 'btn btn-primary mt-3';
        confirmButton.id = 'confirm-button';
        $('.payment-element').append(confirmButton);
        
        confirmButton.addEventListener('click', async () => {
            elements.submit()
            const { error } = await stripe.confirmPayment({
                elements,
                clientSecret: clientSecret,
                confirmParams: {
                    return_url: window.location.origin + '/orders/payment-success/',
                },
            });
            
            if (error) {
                alert(error.message);
            }
        });
    }


    $('#buy-item-button').click(async function() {
        const itemId = $(this).data('item-id');
        const url = `/orders/buy/item/${itemId}/`;
        await initiateStripeCheckout(url);    
    });

    $('#buy-order-button').click(async function() {
        const orderId = $(this).data('order-id');
        const url = `/orders/buy/order/${orderId}/`;
        await initiateStripeCheckout(url);
    });
    
    $('#order-payment-button').click(async function() {
        const orderId = $(this).data('order-id');
        const url = `/orders/create-payment-intent/order/${orderId}/`;
        await handleStripePayment(url, 'order-payment-button');
    });

    $('#item-payment-button').click(async function() {
        const itemId = $(this).data('item-id');
        const url = `/orders/create-payment-intent/item/${itemId}/`;
        await handleStripePayment(url, 'item-payment-button');
    });
    
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