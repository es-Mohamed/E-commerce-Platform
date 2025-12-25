// Faster-Parts/core/static/core/js/quantity_control.js

document.addEventListener('DOMContentLoaded', function() {
    const quantityInput = document.getElementById('quantity-input');
    const decrementBtn = document.getElementById('decrement-btn');
    const incrementBtn = document.getElementById('increment-btn');

    if (quantityInput && decrementBtn && incrementBtn) {
        decrementBtn.addEventListener('click', function() {
            let currentValue = parseInt(quantityInput.value) || 0;
            if (currentValue > 1) {
                quantityInput.value = currentValue - 1;
            }
        });

        incrementBtn.addEventListener('click', function() {
            let currentValue = parseInt(quantityInput.value) || 0;
            quantityInput.value = currentValue + 1;
        });

        // Ensure the input value is always valid
        quantityInput.addEventListener('input', function() {
            let currentValue = parseInt(quantityInput.value) || 1;
            if (currentValue < 1) {
                quantityInput.value = 1;
            }
        });
    }
});