// Markethub Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize cart functionality
    initializeCart();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize rating display
    initializeRatings();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize image lazy loading
    initializeLazyLoading();

    // Initialize interactive ratings
    initializeInteractiveRatings();
});

// Cart Management
function initializeCart() {
    const cartButtons = document.querySelectorAll('.add-to-cart');
    const cartBadge = document.querySelector('.cart-badge');
    
    cartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const productName = this.dataset.productName;
            
            addToCart(productId, productName, this);
        });
    });
    
    // Quantity controls in cart
    const quantityButtons = document.querySelectorAll('.quantity-btn');
    quantityButtons.forEach(button => {
        button.addEventListener('click', function() {
            const action = this.dataset.action;
            const input = this.parentElement.querySelector('.quantity-input');
            const currentValue = parseInt(input.value);
            
            if (action === 'increase') {
                input.value = currentValue + 1;
            } else if (action === 'decrease' && currentValue > 1) {
                input.value = currentValue - 1;
            }
            
            updateCartItem(input.dataset.productId, input.value);
        });
    });
    
    // Remove from cart buttons
    const removeButtons = document.querySelectorAll('.remove-from-cart');
    removeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            removeFromCart(productId, this);
        });
    });
}

function addToCart(productId, productName, button) {
    // Show loading state
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="loading"></span> Добавление...';
    button.disabled = true;
    
    // Make AJAX request to add to cart
    fetch(`/orders/add/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'product_id': productId,
            'quantity': 1
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update cart badge
            updateCartBadge(data.cart_count);
            
            // Show success message
            showNotification(`${productName} добавлен в корзину`, 'success');
            
            // Update button text
            button.innerHTML = '<i class="fas fa-check"></i> Добавлено';
            button.classList.remove('btn-primary');
            button.classList.add('btn-success');
            
            // Reset button after 2 seconds
            setTimeout(() => {
                button.innerHTML = originalText;
                button.classList.remove('btn-success');
                button.classList.add('btn-primary');
                button.disabled = false;
            }, 2000);
        } else {
            showNotification('Ошибка при добавлении в корзину', 'error');
            button.innerHTML = originalText;
            button.disabled = false;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Ошибка при добавлении в корзину', 'error');
        button.innerHTML = originalText;
        button.disabled = false;
    });
}

function removeFromCart(productId, button) {
    if (confirm('Удалить товар из корзины?')) {
        fetch(`/orders/remove/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove cart item from DOM
                const cartItem = button.closest('.cart-item');
                cartItem.remove();
                
                // Update cart badge
                updateCartBadge(data.cart_count);
                
                // Update total
                updateCartTotal(data.cart_total);
                
                showNotification('Товар удален из корзины', 'success');
            } else {
                showNotification('Ошибка при удалении товара', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Ошибка при удалении товара', 'error');
        });
    }
}

function updateCartItem(productId, quantity) {
    fetch(`/orders/update/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'quantity': quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update item total
            const itemTotal = document.querySelector(`[data-item-total="${productId}"]`);
            if (itemTotal) {
                itemTotal.textContent = data.item_total + ' ₽';
            }
            
            // Update cart total
            updateCartTotal(data.cart_total);
            
            // Update cart badge
            updateCartBadge(data.cart_count);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function updateCartBadge(count) {
    const cartBadge = document.querySelector('.cart-badge');
    if (cartBadge) {
        cartBadge.textContent = count;
        if (count > 0) {
            cartBadge.style.display = 'flex';
        } else {
            cartBadge.style.display = 'none';
        }
    }
}

function updateCartTotal(total) {
    const cartTotal = document.querySelector('.cart-total');
    if (cartTotal) {
        cartTotal.textContent = total + ' ₽';
    }
}

// Search and Filter Functionality
function initializeSearch() {
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('.search-input');
    const priceMinInput = document.querySelector('#price_min');
    const priceMaxInput = document.querySelector('#price_max');
    
    if (searchForm) {
        // Auto-submit form on input change with debounce
        let searchTimeout;
        
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    searchForm.submit();
                }, 500);
            });
        }
        
        if (priceMinInput || priceMaxInput) {
            [priceMinInput, priceMaxInput].forEach(input => {
                if (input) {
                    input.addEventListener('change', function() {
                        searchForm.submit();
                    });
                }
            });
        }
    }
    
    // Clear search button
    const clearSearchBtn = document.querySelector('.clear-search');
    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', function() {
            if (searchInput) searchInput.value = '';
            if (priceMinInput) priceMinInput.value = '';
            if (priceMaxInput) priceMaxInput.value = '';
            searchForm.submit();
        });
    }
}

// Rating Display
function initializeRatings() {
    const ratings = document.querySelectorAll('.rating');
    
    ratings.forEach(rating => {
        const score = parseFloat(rating.dataset.rating);
        const stars = rating.querySelectorAll('.star');
        
        stars.forEach((star, index) => {
            if (index < Math.floor(score)) {
                star.classList.add('fas');
                star.classList.remove('far');
            } else if (index < score) {
                star.classList.add('fas');
                star.classList.remove('far');
                star.style.background = `linear-gradient(90deg, #ffc107 ${(score - index) * 100}%, #dee2e6 ${(score - index) * 100}%)`;
                star.style.webkitBackgroundClip = 'text';
                star.style.webkitTextFillColor = 'transparent';
            } else {
                star.classList.add('far');
                star.classList.remove('fas');
            }
        });
    });
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        });
    });
    
    // Real-time validation for dotted inputs
    const dottedInputs = document.querySelectorAll('.dotted-input');
    dottedInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.checkValidity()) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            }
        });
    });
}

// Image Lazy Loading
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Notification System
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.minWidth = '300px';
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Utility Functions
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

// Image Preview for Forms
function previewImage(input, previewId) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById(previewId);
            if (preview) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Smooth Scroll
function smoothScroll(target) {
    document.querySelector(target).scrollIntoView({
        behavior: 'smooth'
    });
}

// Mobile Menu Toggle
function toggleMobileMenu() {
    const mobileMenu = document.querySelector('.navbar-collapse');
    if (mobileMenu) {
        mobileMenu.classList.toggle('show');
    }
}

// Price Formatting
function formatPrice(price) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 0
    }).format(price);
}

// Date Formatting
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Enhanced Rating System
function initializeInteractiveRatings() {
    const ratingInputs = document.querySelectorAll('.rating-input');
    
    ratingInputs.forEach(ratingInput => {
        const stars = ratingInput.querySelectorAll('.rating-star');
        const radioInputs = ratingInput.querySelectorAll('input[type="radio"]');
        
        stars.forEach((star, index) => {
            star.addEventListener('click', function() {
                const rating = this.dataset.rating;
                
                // Check corresponding radio button
                const radioInput = ratingInput.querySelector(`input[value="${rating}"]`);
                if (radioInput) {
                    radioInput.checked = true;
                }
                
                // Update visual state
                updateStarDisplay(stars, rating);
            });
            
            star.addEventListener('mouseenter', function() {
                const rating = this.dataset.rating;
                updateStarDisplay(stars, rating);
            });
        });
        
        ratingInput.addEventListener('mouseleave', function() {
            const checkedInput = ratingInput.querySelector('input[type="radio"]:checked');
            const checkedRating = checkedInput ? checkedInput.value : 0;
            updateStarDisplay(stars, checkedRating);
        });
    });
}

function updateStarDisplay(stars, rating) {
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.add('filled');
            star.innerHTML = '<i class="fas fa-star"></i>';
        } else {
            star.classList.remove('filled');
            star.innerHTML = '<i class="far fa-star"></i>';
        }
    });
}
