// Common admin panel JavaScript functions

// Global toast notification function
function showAlert(message, type = 'info', duration = 5000) {
    // Remove existing alerts
    const existingAlert = document.querySelector('.alert-floating');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show alert-floating position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-dismiss after duration
    if (duration > 0) {
        setTimeout(() => {
            if (alertDiv) {
                alertDiv.remove();
            }
        }, duration);
    }
}

// Loading spinner utility
function showLoading(element, text = 'Loading...') {
    const originalContent = element.innerHTML;
    element.innerHTML = `
        <i class="fas fa-spinner fa-spin me-2"></i>${text}
    `;
    element.disabled = true;
    
    return () => {
        element.innerHTML = originalContent;
        element.disabled = false;
    };
}

// Confirmation dialog utility
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// API request helper
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || `HTTP ${response.status}`);
        }
        
        return data;
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Format timestamps
function formatTimestamp(timestamp) {
    return new Date(timestamp).toLocaleString();
}

// Copy to clipboard utility
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Copied to clipboard!', 'success', 2000);
    }).catch(err => {
        console.error('Copy failed:', err);
        showAlert('Copy failed', 'danger', 2000);
    });
}

// Dark theme toggle (if needed)
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Initialize theme from localStorage
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
}

// Real-time status updates
class StatusMonitor {
    constructor(updateInterval = 30000) {
        this.updateInterval = updateInterval;
        this.isRunning = false;
        this.callbacks = [];
    }
    
    addCallback(callback) {
        this.callbacks.push(callback);
    }
    
    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.update();
        this.intervalId = setInterval(() => this.update(), this.updateInterval);
    }
    
    stop() {
        this.isRunning = false;
        if (this.intervalId) {
            clearInterval(this.intervalId);
        }
    }
    
    async update() {
        try {
            const status = await apiRequest('/admin/api/metrics');
            this.callbacks.forEach(callback => callback(status));
        } catch (error) {
            console.error('Status update failed:', error);
        }
    }
}

// Initialize status monitor
const statusMonitor = new StatusMonitor();

// Auto-save form utility
class AutoSaveForm {
    constructor(formId, saveUrl, saveInterval = 30000) {
        this.form = document.getElementById(formId);
        this.saveUrl = saveUrl;
        this.saveInterval = saveInterval;
        this.isDirty = false;
        this.lastSaved = null;
        
        if (this.form) {
            this.initialize();
        }
    }
    
    initialize() {
        // Track form changes
        this.form.addEventListener('input', () => {
            this.isDirty = true;
            this.showUnsavedIndicator();
        });
        
        // Auto-save periodically
        setInterval(() => {
            if (this.isDirty) {
                this.save();
            }
        }, this.saveInterval);
        
        // Save before page unload
        window.addEventListener('beforeunload', (e) => {
            if (this.isDirty) {
                e.preventDefault();
                e.returnValue = 'You have unsaved changes. Are you sure you want to leave?';
            }
        });
    }
    
    async save() {
        if (!this.isDirty) return;
        
        try {
            const formData = new FormData(this.form);
            await apiRequest(this.saveUrl, {
                method: 'POST',
                body: formData
            });
            
            this.isDirty = false;
            this.lastSaved = new Date();
            this.showSavedIndicator();
            
        } catch (error) {
            showAlert('Auto-save failed', 'warning');
            console.error('Auto-save error:', error);
        }
    }
    
    showUnsavedIndicator() {
        const indicator = document.getElementById('save-indicator');
        if (indicator) {
            indicator.innerHTML = '<i class="fas fa-circle text-warning me-1"></i>Unsaved changes';
        }
    }
    
    showSavedIndicator() {
        const indicator = document.getElementById('save-indicator');
        if (indicator) {
            indicator.innerHTML = '<i class="fas fa-check-circle text-success me-1"></i>Saved';
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    initializeTheme();
    
    // Start status monitoring on dashboard
    if (document.querySelector('[data-page="dashboard"]')) {
        statusMonitor.start();
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Cleanup when page unloads
window.addEventListener('beforeunload', function() {
    statusMonitor.stop();
});
