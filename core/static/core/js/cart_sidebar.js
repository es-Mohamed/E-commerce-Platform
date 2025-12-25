// Faster-Parts/core/static/core/js/cart_sidebar.js

document.addEventListener('DOMContentLoaded', function() {
    const cartIcon = document.getElementById('cart-icon');
    const cartSidebar = document.getElementById('cart-sidebar');
    const closeSidebarBtn = document.getElementById('close-sidebar');
    const sidebarOverlay = document.getElementById('sidebar-overlay');
    const cartContent = document.getElementById('cart-content');
    const cartTotal = document.getElementById('cart-total');
    const cartItemCountSpan = document.getElementById('cart-item-count');

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Function to open the sidebar
    function openSidebar() {
        if (!cartSidebar || !sidebarOverlay) return;
        // Logic to handle both LTR and RTL directions
        if (document.documentElement.dir === 'rtl') {
            cartSidebar.classList.remove('translate-x-full');
        } else {
            cartSidebar.classList.remove('-translate-x-full');
        }
        sidebarOverlay.classList.remove('hidden');
        document.body.classList.add('overflow-hidden');
        fetchCartData(); // Fetch cart data when sidebar opens
    }

    // Function to close the sidebar
    function closeSidebar() {
        if (!cartSidebar || !sidebarOverlay) return;
         if (document.documentElement.dir === 'rtl') {
            cartSidebar.classList.add('translate-x-full');
        } else {
            cartSidebar.classList.add('-translate-x-full');
        }
        sidebarOverlay.classList.add('hidden');
        document.body.classList.remove('overflow-hidden');
    }

    // Function to update the cart item count on the icon
    function updateCartItemCount(count) {
        if (!cartItemCountSpan) return;
        if (count > 0) {
            cartItemCountSpan.textContent = count;
            cartItemCountSpan.classList.remove('hidden');
        } else {
            cartItemCountSpan.textContent = '0';
            cartItemCountSpan.classList.add('hidden');
        }
    }
    
    // Centralized function to send ALL cart updates (add, update, remove)
    async function sendCartUpdateRequest(url, formData) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest' // Helps Django identify AJAX requests
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                console.log(data.message); // Log success message
                fetchCartData(); // Re-fetch all cart data to update UI perfectly
            } else {
                alert('Error: ' + (data.message || 'An unknown error occurred.'));
                fetchCartData(); // Re-fetch to revert any optimistic UI changes
            }
        } catch (error) {
            console.error('Error sending cart update:', error);
            alert('An error occurred. Please try again.');
            fetchCartData(); // Re-fetch to revert
        }
    }

    // Function to fetch and display cart data in the sidebar
    async function fetchCartData() {
        // The cartTotal element is no longer updated separately.
        if (!cartContent || !cartSidebar) return;

        cartContent.innerHTML = '<p class="text-gray-500">Loading cart...</p>';

        const getDataURL = cartSidebar.dataset.getDataUrl;
        if (!getDataURL) {
            console.error('Get Cart Data URL is not defined in HTML.');
            return;
        }

        try {
            const response = await fetch(getDataURL);
            const data = await response.json();

            if (data.success) {
                updateCartItemCount(data.total_items_in_cart);
                if (data.cart_exists && data.cart_items.length > 0) {
                    const isRtl = document.documentElement.dir === 'rtl';
                    const flexDirection = isRtl ? 'flex-row-reverse' : 'flex-row';
                    
                    let contentHTML = data.cart_items.map(item => `
                        <div class="flex ${flexDirection} items-center justify-between mb-4 pb-4 border-b border-gray-200">
                            <div class="flex items-center space-x-4 ${isRtl ? 'space-x-reverse' : ''}">
                                ${item.item_image_url 
                                    ? `<img src="${item.item_image_url}" alt="${item.item_name}" class="w-16 h-16 object-cover rounded-md">` 
                                    : `<div class="w-16 h-16 bg-gray-300 rounded-md flex items-center justify-center text-gray-500">No Image</div>`
                                }
                                <div class="flex flex-col">
                                    <h3 class="font-semibold text-gray-800">${item.item_name}</h3>
                                    <p class="text-sm text-gray-600">Total: ${item.total_price} EGP</p>
                                </div>
                            </div>
                            <div class="flex items-center space-x-2 ${isRtl ? 'space-x-reverse' : ''}">
                                <div class="flex items-center">
                                    <button class="qty-btn px-2 py-1 bg-gray-200 text-gray-700 rounded-l" data-action="decrement" data-item-id="${item.item_id}">-</button>
                                    <input type="number" value="${item.quantity}" min="1" class="w-12 text-center border-t border-b border-gray-300 py-1 text-sm" readonly>
                                    <button class="qty-btn px-2 py-1 bg-gray-200 text-gray-700 rounded-r" data-action="increment" data-item-id="${item.item_id}">+</button>
                                </div>
                                <button class="remove-item-btn p-2 bg-red-500 text-white rounded-md text-sm" data-item-id="${item.item_id}">
                                    <i class="fa-solid fa-trash-can"></i>
                                </button>
                            </div>
                        </div>
                    `).join('');

                    // Dynamically add the total and the request button after the items
                    contentHTML += `
                        <div class="mt-6 pt-4 border-t border-gray-300">
                            <p class="text-lg font-bold ${isRtl ? 'text-right' : 'text-left'}">Total: ${data.total_cart_price} EGP</p>
                            <button id="request-order-btn" class="w-full mt-4 py-2 px-4 bg-blue-600 text-white text-center rounded-md hover:bg-blue-700">Request Order</button>
                        </div>
                    `;
                    cartContent.innerHTML = contentHTML;

                } else {
                    cartContent.innerHTML = `<p class="text-gray-500">${data.message || 'Your cart is empty.'}</p>`;
                }
            } else {
                cartContent.innerHTML = '<p class="text-red-500">Error loading cart.</p>';
            }
        } catch (error) {
            console.error('Error fetching cart data:', error);
            cartContent.innerHTML = '<p class="text-red-500">Could not load cart data.</p>';
        }
    }
    
    // === Event Delegation for ALL dynamically created buttons inside cartContent ===
    cartContent.addEventListener('click', async function(e) {
        const target = e.target;
        
        // Handle quantity buttons (+/-)
        const qtyBtn = target.closest('.qty-btn');
        if (qtyBtn) {
            const itemId = qtyBtn.dataset.itemId;
            const action = qtyBtn.dataset.action;
            const quantityInput = qtyBtn.parentElement.querySelector('input[type="number"]');
            let currentQuantity = parseInt(quantityInput.value) || 0;
            
            let newQuantity;
            if (action === 'increment') {
                newQuantity = currentQuantity + 1;
            } else if (action === 'decrement') {
                newQuantity = currentQuantity > 1 ? currentQuantity - 1 : 0;
            }

            const updateUrlTemplate = cartSidebar.dataset.updateUrl;
            if (!updateUrlTemplate) {
                console.error('Update Cart URL is not defined in HTML.');
                return;
            }
            const url = updateUrlTemplate.replace('0', itemId);

            const formData = new FormData();
            formData.append('quantity', newQuantity);
            
            sendCartUpdateRequest(url, formData);
        }

        // Handle remove button
        const removeBtn = target.closest('.remove-item-btn');
        if (removeBtn) {
            const itemId = removeBtn.dataset.itemId;
             if (confirm("Are you sure you want to remove this item?")) {
                const removeUrlTemplate = cartSidebar.dataset.removeUrl;
                if (!removeUrlTemplate) {
                    console.error('Remove Cart URL is not defined in HTML.');
                    return;
                }
                const url = removeUrlTemplate.replace('0', itemId);
                sendCartUpdateRequest(url, new FormData());
            }
        }

        // Handle Request Order button
        const requestBtn = target.closest('#request-order-btn');
        if (requestBtn) {
            e.preventDefault();
            
            const createOrderUrl = cartSidebar.dataset.createOrderUrl;
            if (!createOrderUrl) {
                console.error('Create Order URL is not defined in HTML.');
                alert('Cannot process request: Configuration error.');
                return;
            }

            requestBtn.disabled = true;
            const originalButtonText = requestBtn.textContent;
            requestBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

            try {
                const response = await fetch(createOrderUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                });

                const data = await response.json();

                if (data.success) {
                    alert(data.message);
                    fetchCartData();
                    window.location.href = data.conversation_url;
                } else {
                    alert('Error: ' + (data.message || 'Could not process your request.'));
                    requestBtn.disabled = false;
                    requestBtn.textContent = originalButtonText;
                }
            } catch (error) {
                console.error('Error sending order request:', error);
                alert('An unexpected error occurred. Please try again.');
                requestBtn.disabled = false;
                requestBtn.textContent = originalButtonText;
            }
        }
    });

    // Handle "Add to Cart" form submissions
    document.querySelectorAll('form[action*="/cart/add/"]').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const url = this.action;
            const formData = new FormData(this);
            sendCartUpdateRequest(url, formData);
            openSidebar();
        });
    });

    // Event Listeners for sidebar toggle
    if (cartIcon) {
        cartIcon.addEventListener('click', function(e) {
            e.preventDefault();
            openSidebar();
        });
    }
    if (closeSidebarBtn) {
        closeSidebarBtn.addEventListener('click', closeSidebar);
    }
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', closeSidebar);
    }

    // Initial fetch of cart data to update the icon count on page load
    fetchCartData();
});