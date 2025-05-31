    $(document).ready(function() {
        // Initialize cart
        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        
        // Add to Cart functionality
        $('.add-to-cart').click(function() {
            const itemId = $(this).data('item-id');
            const card = $(this).closest('.card');
            const itemName = card.data('item-name');
            const itemPrice = parseFloat(card.data('item-price'));
			const itemCurrency = card.data('item-currency') || 'usd';
            // Check if item already in cart
            const existingItem = cart.find(item => item.id === itemId);
            if (existingItem) {
                existingItem.quantity += 1;
                existingItem.name = itemName;
                existingItem.price = itemPrice;
				existingItem.currency = itemCurrency;  // Update name in case it changes
            } else {
                cart.push({
                    id: itemId,
                    name: itemName,
                    price: itemPrice,
					currency: itemCurrency,
                    quantity: 1
                });
            }
            
            localStorage.setItem('cart', JSON.stringify(cart));
            updateCartBadge();
            showToast('Item added to cart');
        });
        
        // Add this function to your existing script
    function displayCartItems() {
        const cartItemsContainer = $('#cart-items');
        cartItemsContainer.empty();
        if (cart.length === 0) {
            cartItemsContainer.html('<p>Your cart is empty</p>');
            return;
        }
        
        let html = '<ul class="list-group mb-3">';
        let total = 0;
        
        cart.forEach(item => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            
            html += `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <h6>${item.name}</h6>
                        <small>$${item.price} x ${item.quantity}</small>
                    </div>
                    <div>
                        <span class="fw-bold">$${itemTotal.toFixed(2)}</span>
                        <button class="btn btn-sm btn-outline-danger ms-2 remove-item" data-item-id="${item.id}">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </li>
            `;
        });
        
        html += `
            <li class="list-group-item d-flex justify-content-between fw-bold">
                <span>Total</span>
                <span>$${total.toFixed(2)}</span>
            </li>
        </ul>`;
        
        cartItemsContainer.html(html);
        
        // Add event listener for remove buttons
        $('.remove-item').click(function() {
            const itemId = $(this).data('item-id');
            cart = cart.filter(item => item.id !== itemId);
            localStorage.setItem('cart', JSON.stringify(cart));
            displayCartItems();
            updateCartBadge();
            showToast('Item removed from cart');
        });
    }


    $('#cart-button').click(function() {
        console.log("Cart icon clicked, displaying cart items");
        displayCartItems();
        $('#cartModal').modal('show');
    });

    // Checkout button handler
    $('#checkout-button').click(async function() {
        try {
			const csrftoken = getCookie('csrftoken');
			console.log("TOKEN", csrftoken);
            const response = await fetch('checkout/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
					'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ items: cart })
            });
            
            const session = await response.json();
            const sessionId = session.session.id
            // Redirect to Stripe Checkout
            const result = await stripe.redirectToCheckout({ sessionId: sessionId });
            
            if (result.error) {
                showToast(result.error.message);
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('An error occurred during checkout');
        }
    });
    // Update cart badge
    function updateCartBadge() {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        $('#cart-badge').text(totalItems).toggle(totalItems > 0);
    }
    
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
    
    // Initialize cart badge
    updateCartBadge();
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