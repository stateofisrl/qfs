/* Main JavaScript */

const API_BASE_URL = '/api';
const TOKEN = localStorage.getItem('token');

// Fetch wrapper
async function fetchAPI(endpoint, options = {}) {
    // When sending FormData, do not set Content-Type header
    const isFormData = options.body instanceof FormData;
    const headers = {
        'X-CSRFToken': getCookie('csrftoken'),
        ...options.headers,
    };
    if (!isFormData) headers['Content-Type'] = 'application/json';

    if (TOKEN) {
        headers['Authorization'] = `Token ${TOKEN}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers,
            credentials: 'same-origin',
        });

        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '/login/';
            }
            const errorText = await response.text();
            console.error('API Error Response:', errorText);
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showAlert('An error occurred. Please try again.', 'danger');
        throw error;
    }
}

// Logout handler - update nav link if present
document.addEventListener('DOMContentLoaded', function(){
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e){
            e.preventDefault();
            // Clear any leftover token used by API clients
            try { localStorage.removeItem('token'); } catch (_) {}
            // Use server-side session logout to avoid session mix-ups
            window.location.href = '/logout/';
        });
    }
});

// CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Show Alert
function showAlert(message, type = 'info') {
    const alertsContainer = document.querySelector('.alerts-container') || createAlertsContainer();
    const alertId = `alert-${Date.now()}`;
    
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert" id="${alertId}">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertsContainer.insertAdjacentHTML('beforeend', alertHTML);
    
    setTimeout(() => {
        const alert = document.getElementById(alertId);
        if (alert) {
            alert.remove();
        }
    }, 5000);
}

function createAlertsContainer() {
    const container = document.createElement('div');
    container.className = 'alerts-container container mt-3';
    document.querySelector('main').insertAdjacentElement('afterbegin', container);
    return container;
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    });
}

// Format datetime
function formatDateTime(dateString) {
    return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
}

// Get status badge
function getStatusBadge(status) {
    const badges = {
        pending: '<span class="badge badge-pending">Pending</span>',
        approved: '<span class="badge badge-approved">Approved</span>',
        rejected: '<span class="badge badge-rejected">Rejected</span>',
        active: '<span class="badge badge-active">Active</span>',
        completed: '<span class="badge badge-completed">Completed</span>',
        processing: '<span class="badge bg-info">Processing</span>',
        closed: '<span class="badge bg-secondary">Closed</span>',
        in_progress: '<span class="badge bg-warning">In Progress</span>',
    };
    return badges[status] || `<span class="badge bg-secondary">${status}</span>`;
}
// Alert Modal System
function showAlertModal(message, type = 'info') {
    // Create modal backdrop with inline styles
    const backdrop = document.createElement('div');
    backdrop.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        opacity: 0;
        transition: opacity 0.3s ease-in-out;
    `;
    
    // Determine icon and colors based on type
    let icon = '';
    let bgColor = '#f0fdf4';
    let borderColor = '#86efac';
    let textColor = '#166534';
    let buttonColor = '#16a34a';
    let buttonHover = '#15803d';
    
    if (type === 'success') {
        icon = '<svg class="w-16 h-16" style="color: #16a34a; margin: 0 auto;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>';
        bgColor = '#f0fdf4';
        borderColor = '#86efac';
        textColor = '#166534';
        buttonColor = '#16a34a';
        buttonHover = '#15803d';
    } else if (type === 'error' || type === 'danger') {
        icon = '<svg class="w-16 h-16" style="color: #dc2626; margin: 0 auto;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4v.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>';
        bgColor = '#fef2f2';
        borderColor = '#fca5a5';
        textColor = '#7f1d1d';
        buttonColor = '#dc2626';
        buttonHover = '#b91c1c';
    } else if (type === 'warning') {
        icon = '<svg class="w-16 h-16" style="color: #ca8a04; margin: 0 auto;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4v2m0 4v.01M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"></path></svg>';
        bgColor = '#fefce8';
        borderColor = '#fde047';
        textColor = '#713f12';
        buttonColor = '#ca8a04';
        buttonHover = '#a16207';
    } else {
        icon = '<svg class="w-16 h-16" style="color: #2563eb; margin: 0 auto;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>';
        bgColor = '#eff6ff';
        borderColor = '#93c5fd';
        textColor = '#1e3a8a';
        buttonColor = '#2563eb';
        buttonHover = '#1d4ed8';
    }
    
    // Create modal content
    const modal = document.createElement('div');
    modal.style.cssText = `
        background-color: ${bgColor};
        border: 2px solid ${borderColor};
        border-radius: 12px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        padding: 32px;
        max-width: 448px;
        width: 100%;
        margin: 0 16px;
        opacity: 0;
        transform: scale(0.95);
        transition: all 0.3s ease-in-out;
    `;
    
    modal.innerHTML = `
        <div style="text-align: center;">
            ${icon}
            <h2 style="font-size: 24px; font-weight: bold; color: ${textColor}; margin-top: 16px; margin-bottom: 8px;">Alert</h2>
            <p style="color: #374151; margin-bottom: 24px;">${message}</p>
            <button style="width: 100%; background-color: ${buttonColor}; color: white; font-weight: bold; padding: 12px 24px; border-radius: 8px; border: none; cursor: pointer; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1); transition: all 0.2s;">
                OK
            </button>
        </div>
    `;
    
    // Set button hover effect
    const button = modal.querySelector('button');
    button.addEventListener('mouseover', function() {
        this.style.backgroundColor = buttonHover;
        this.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
    });
    button.addEventListener('mouseout', function() {
        this.style.backgroundColor = buttonColor;
        this.style.boxShadow = '0 1px 3px 0 rgba(0, 0, 0, 0.1)';
    });
    
    backdrop.appendChild(modal);
    document.body.appendChild(backdrop);
    
    // Close on button click or backdrop click
    button.addEventListener('click', function() {
        backdrop.style.opacity = '0';
        modal.style.opacity = '0';
        modal.style.transform = 'scale(0.95)';
        setTimeout(() => {
            backdrop.remove();
        }, 300);
    });
    
    backdrop.addEventListener('click', function(e) {
        if (e.target === backdrop) {
            backdrop.style.opacity = '0';
            modal.style.opacity = '0';
            modal.style.transform = 'scale(0.95)';
            setTimeout(() => {
                backdrop.remove();
            }, 300);
        }
    });
    
    // Add open animation - trigger reflow to enable transition
    setTimeout(() => {
        backdrop.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        backdrop.style.opacity = '1';
        modal.style.opacity = '1';
        modal.style.transform = 'scale(1)';
    }, 10);
}

// Check for server-side alerts and display them on page load
document.addEventListener('DOMContentLoaded', function() {
    const successAlert = document.querySelector('[data-alert-success]');
    const errorAlert = document.querySelector('[data-alert-error]');
    
    if (successAlert) {
        const message = successAlert.getAttribute('data-alert-success');
        if (message && message.trim() !== '') {
            showAlertModal(message, 'success');
        }
        successAlert.remove();
    }
    
    if (errorAlert) {
        const message = errorAlert.getAttribute('data-alert-error');
        if (message && message.trim() !== '') {
            showAlertModal(message, 'error');
        }
        errorAlert.remove();
    }
});