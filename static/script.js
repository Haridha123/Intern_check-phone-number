// WhatsApp Checker JavaScript
console.log('WhatsApp Checker script loaded');

class WhatsAppChecker {
    constructor() {
        console.log('WhatsAppChecker initialized');
        this.sessionInitialized = false;
        this.initializeElements();
        this.attachEventListeners();
        this.checkSessionStatus();
    }

    initializeElements() {
        this.elements = {
            sessionStatus: document.getElementById('sessionStatus'),
            initBtn: document.getElementById('initBtn'),
            sessionInfo: document.getElementById('sessionInfo'),
            singleNumber: document.getElementById('singleNumber'),
            checkSingle: document.getElementById('checkSingle'),
            singleResult: document.getElementById('singleResult'),
            batchNumbers: document.getElementById('batchNumbers'),
            checkBatch: document.getElementById('checkBatch'),
            batchProgress: document.getElementById('batchProgress'),
            progressFill: document.getElementById('progressFill'),
            progressText: document.getElementById('progressText'),
            batchResults: document.getElementById('batchResults')
        };
        console.log('Elements initialized', this.elements);
    }

    attachEventListeners() {
        console.log('Attaching event listeners');
        
        if (this.elements.initBtn) {
            this.elements.initBtn.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('Initialize button clicked');
                this.initializeSession();
            });
        }
        
        if (this.elements.checkSingle) {
            this.elements.checkSingle.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('Check single button clicked');
                this.checkSingleNumber();
            });
        }
        
        if (this.elements.checkBatch) {
            this.elements.checkBatch.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('Check batch button clicked');
                this.checkBatchNumbers();
            });
        }
    }

    async checkSessionStatus() {
        console.log('Checking session status');
        try {
            const response = await fetch('/api/session-status');
            const data = await response.json();
            console.log('Session status:', data);
            
            if (data.initialized) {
                this.updateSessionStatus('connected', 'Session Ready', 'fas fa-check-circle');
                this.sessionInitialized = true;
                if (this.elements.sessionInfo) {
                    this.elements.sessionInfo.style.display = 'flex';
                }
                if (this.elements.checkSingle) this.elements.checkSingle.disabled = false;
                if (this.elements.checkBatch) this.elements.checkBatch.disabled = false;
            } else {
                this.updateSessionStatus('error', 'Session Not Ready', 'fas fa-exclamation-circle');
            }
        } catch (error) {
            console.error('Error checking session status:', error);
            this.updateSessionStatus('error', 'Connection Error', 'fas fa-exclamation-triangle');
        }
    }

    async initializeSession() {
        console.log('Initializing session...');
        
        if (this.elements.initBtn) {
            this.elements.initBtn.disabled = true;
            this.elements.initBtn.innerHTML = '<i class=\"fas fa-spinner fa-spin\"></i> Initializing...';
        }
        
        try {
            const response = await fetch('/api/initialize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            const data = await response.json();
            console.log('Initialize response:', data);
            
            if (data.success) {
                this.updateSessionStatus('connected', 'Session Ready', 'fas fa-check-circle');
                this.sessionInitialized = true;
                if (this.elements.sessionInfo) {
                    this.elements.sessionInfo.style.display = 'flex';
                }
                if (this.elements.checkSingle) this.elements.checkSingle.disabled = false;
                if (this.elements.checkBatch) this.elements.checkBatch.disabled = false;
                this.showNotification('Session initialized successfully!', 'success');
            } else {
                this.showNotification('Failed to initialize session', 'error');
            }
        } catch (error) {
            console.error('Initialize error:', error);
            this.showNotification('Connection error', 'error');
        } finally {
            if (this.elements.initBtn) {
                this.elements.initBtn.disabled = false;
                this.elements.initBtn.innerHTML = '<i class=\"fas fa-play\"></i> Initialize WhatsApp Session';
            }
        }
    }

    async checkSingleNumber() {
        const number = this.elements.singleNumber ? this.elements.singleNumber.value.trim() : '';
        if (!number) {
            this.showNotification('Please enter a phone number', 'error');
            return;
        }

        if (this.elements.checkSingle) {
            this.elements.checkSingle.disabled = true;
            this.elements.checkSingle.innerHTML = '<i class=\"fas fa-spinner fa-spin\"></i> Checking...';
        }
        
        if (this.elements.singleResult) {
            this.elements.singleResult.innerHTML = '';
        }

        try {
            const response = await fetch('/api/check-single', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ number })
            });

            const data = await response.json();
            console.log('Single check response:', data);
            
            if (data.error) {
                this.displaySingleResult(number, false, data.error, 'error');
            } else {
                this.displaySingleResult(data.number, data.registered, data.message, data.registered ? 'success' : 'info');
            }
        } catch (error) {
            console.error('Single check error:', error);
            this.displaySingleResult(number, false, 'Connection error', 'error');
        } finally {
            if (this.elements.checkSingle) {
                this.elements.checkSingle.disabled = false;
                this.elements.checkSingle.innerHTML = '<i class=\"fas fa-search\"></i> Check Number';
            }
        }
    }

    async checkBatchNumbers() {
        const numbersText = this.elements.batchNumbers ? this.elements.batchNumbers.value.trim() : '';
        if (!numbersText) {
            this.showNotification('Please enter phone numbers', 'error');
            return;
        }

        const numbers = numbersText.split('\n').filter(n => n.trim());
        if (numbers.length === 0) {
            this.showNotification('No valid numbers found', 'error');
            return;
        }

        if (this.elements.checkBatch) {
            this.elements.checkBatch.disabled = true;
            this.elements.checkBatch.innerHTML = '<i class=\"fas fa-spinner fa-spin\"></i> Starting...';
        }
        
        if (this.elements.batchProgress) {
            this.elements.batchProgress.style.display = 'block';
        }
        
        if (this.elements.batchResults) {
            this.elements.batchResults.innerHTML = '';
        }

        try {
            const response = await fetch('/api/check-batch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ numbers })
            });

            const data = await response.json();
            
            if (data.error) {
                this.showNotification(data.error, 'error');
                return;
            }

            this.monitorBatchProgress();
        } catch (error) {
            console.error('Batch check error:', error);
            this.showNotification('Failed to start batch check', 'error');
        }
    }

    async monitorBatchProgress() {
        const checkStatus = async () => {
            try {
                const response = await fetch('/api/status');
                const status = await response.json();
                
                this.updateBatchProgress(status.progress, status.total);
                
                if (!status.running) {
                    this.displayBatchResults(status.results);
                    if (this.elements.checkBatch) {
                        this.elements.checkBatch.disabled = false;
                        this.elements.checkBatch.innerHTML = '<i class=\"fas fa-play\"></i> Start Batch Check';
                    }
                    return;
                }
                
                setTimeout(checkStatus, 1000);
            } catch (error) {
                console.error('Error monitoring progress:', error);
                setTimeout(checkStatus, 2000);
            }
        };
        
        checkStatus();
    }

    updateBatchProgress(progress, total) {
        const percentage = total > 0 ? (progress / total) * 100 : 0;
        if (this.elements.progressFill) {
            this.elements.progressFill.style.width = percentage + '%';
        }
        if (this.elements.progressText) {
            this.elements.progressText.textContent = progress + ' / ' + total;
        }
    }

    displaySingleResult(number, registered, message, type) {
        const icon = type === 'success' ? 'fas fa-check' : type === 'error' ? 'fas fa-times' : 'fas fa-info';
        
        if (this.elements.singleResult) {
            this.elements.singleResult.innerHTML = 
                '<div class=\"result-item ' + type + ' fade-in\">' +
                    '<div class=\"result-number\">' + number + '</div>' +
                    '<div class=\"result-status\">' +
                        '<i class=\"' + icon + '\"></i>' +
                        message +
                    '</div>' +
                '</div>';
        }
    }

    displayBatchResults(results) {
        if (!results || results.length === 0) {
            if (this.elements.batchResults) {
                this.elements.batchResults.innerHTML = '<p>No results to display</p>';
            }
            return;
        }

        const html = results.map(result => {
            const type = result.error ? 'error' : result.registered ? 'success' : 'info';
            const icon = type === 'success' ? 'fas fa-check' : type === 'error' ? 'fas fa-times' : 'fas fa-info';
            const message = result.error || result.message || 'Unknown status';
            
            return '<div class=\"result-item ' + type + '\">' +
                      '<div class=\"result-number\">' + result.number + '</div>' +
                      '<div class=\"result-status\">' +
                          '<i class=\"' + icon + '\"></i>' +
                          message +
                      '</div>' +
                   '</div>';
        }).join('');

        if (this.elements.batchResults) {
            this.elements.batchResults.innerHTML = html;
        }
        
        if (this.elements.batchProgress) {
            this.elements.batchProgress.style.display = 'none';
        }
        
        const registered = results.filter(r => r.registered && !r.error).length;
        const errors = results.filter(r => r.error).length;
        
        this.showNotification('Completed: ' + registered + ' registered, ' + (results.length - registered - errors) + ' not registered, ' + errors + ' errors', 'info');
    }

    updateSessionStatus(status, text, icon) {
        if (this.elements.sessionStatus) {
            this.elements.sessionStatus.className = 'session-status ' + status;
            this.elements.sessionStatus.innerHTML = '<i class=\"' + icon + '\"></i><span>' + text + '</span>';
        }
    }

    showNotification(message, type) {
        console.log('Notification:', message, type);
        const notification = document.createElement('div');
        notification.className = 'result-item ' + type + ' fade-in';
        notification.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 1000; max-width: 300px;';
        notification.innerHTML = '<div>' + message + '</div>';
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 3000);
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing WhatsApp Checker');
    new WhatsAppChecker();
});

console.log('Script file loaded completely');