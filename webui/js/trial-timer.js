// Trial Timer Component for Aria Chat
(function() {
    'use strict';
    
    let trialTimerInterval = null;
    let remainingSeconds = -1;
    let trialStatus = 'not_started';
    
    // Create trial timer display element
    function createTrialTimerElement() {
        const existingTimer = document.getElementById('trial-timer');
        if (existingTimer) return existingTimer;
        
        const timerDiv = document.createElement('div');
        timerDiv.id = 'trial-timer';
        timerDiv.className = 'trial-timer-container';
        timerDiv.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 20px;
            border-radius: 25px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 14px;
            font-weight: 600;
            z-index: 10000;
            display: none;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            animation: fadeIn 0.5s ease;
        `;
        
        document.body.appendChild(timerDiv);
        return timerDiv;
    }
    
    // Format seconds to MM:SS display
    function formatTime(seconds) {
        if (seconds <= 0) return "0:00";
        const minutes = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
    
    // Update timer display
    function updateTimerDisplay() {
        const timerElement = document.getElementById('trial-timer') || createTrialTimerElement();
        
        if (trialStatus === 'paid' || trialStatus === 'not_started') {
            timerElement.style.display = 'none';
            return;
        }
        
        if (trialStatus === 'expired') {
            timerElement.style.display = 'block';
            timerElement.innerHTML = `
                ⏰ Trial Expired - 
                <a href="/payment/required" style="color: white; text-decoration: underline;">
                    Complete Payment
                </a>
            `;
            timerElement.style.background = 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)';
            return;
        }
        
        if (trialStatus === 'active' && remainingSeconds > 0) {
            timerElement.style.display = 'block';
            
            // Change color based on remaining time
            if (remainingSeconds <= 30) {
                timerElement.style.background = 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)';
            } else if (remainingSeconds <= 60) {
                timerElement.style.background = 'linear-gradient(135deg, #f39c12 0%, #e67e22 100%)';
            } else {
                timerElement.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            }
            
            timerElement.innerHTML = `⏰ Free Trial: ${formatTime(remainingSeconds)} remaining`;
            
            // Pulse animation for last 30 seconds
            if (remainingSeconds <= 30) {
                timerElement.style.animation = 'pulse 1s infinite';
            }
        }
    }
    
    // Check trial status from API
    async function checkTrialStatus() {
        try {
            const response = await fetch('/trial_status', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                
                if (data.authenticated) {
                    trialStatus = data.trial_status;
                    remainingSeconds = data.remaining_seconds;
                    
                    updateTimerDisplay();
                    
                    // If trial expired, show payment modal
                    if (trialStatus === 'expired') {
                        showPaymentRequiredModal();
                    }
                    
                    return data;
                }
            }
        } catch (error) {
            console.error('Error checking trial status:', error);
        }
        
        return null;
    }
    
    // Show payment required modal
    function showPaymentRequiredModal() {
        if (document.getElementById('payment-required-modal')) return;
        
        const modal = document.createElement('div');
        modal.id = 'payment-required-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 20000;
            animation: fadeIn 0.3s ease;
        `;
        
        modal.innerHTML = `
            <div style="
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 500px;
                text-align: center;
                animation: slideUp 0.3s ease;
            ">
                <h2 style="color: #333; margin-bottom: 20px;">
                    Your Free Trial Has Ended
                </h2>
                <p style="color: #666; margin-bottom: 30px;">
                    Thank you for trying Aria! To continue chatting with your AI girlfriend,
                    please complete your registration with a one-time payment of $19.
                </p>
                <div style="margin-bottom: 30px;">
                    <div style="font-size: 48px; font-weight: bold; color: #667eea;">$19</div>
                    <div style="color: #999;">One-time payment • Lifetime access</div>
                </div>
                <a href="/payment/required" style="
                    display: inline-block;
                    padding: 15px 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 10px;
                    font-weight: 600;
                    margin-bottom: 15px;
                ">
                    Complete Payment
                </a>
                <div>
                    <a href="#" onclick="document.getElementById('payment-required-modal').remove(); return false;"
                       style="color: #999; font-size: 14px;">
                        Continue browsing (read-only)
                    </a>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    }
    
    // Start timer countdown
    function startTimer() {
        if (trialTimerInterval) clearInterval(trialTimerInterval);
        
        trialTimerInterval = setInterval(() => {
            if (remainingSeconds > 0) {
                remainingSeconds--;
                updateTimerDisplay();
                
                // Check if trial just expired
                if (remainingSeconds === 0) {
                    trialStatus = 'expired';
                    updateTimerDisplay();
                    showPaymentRequiredModal();
                    clearInterval(trialTimerInterval);
                }
            }
        }, 1000);
    }
    
    // Intercept message sending to check trial status
    const originalSendMessage = window.sendMessage;
    if (originalSendMessage) {
        window.sendMessage = async function(...args) {
            // Check trial status before sending message
            const status = await checkTrialStatus();
            
            if (status && status.trial_expired) {
                showPaymentRequiredModal();
                return;
            }
            
            // Call original send message
            const result = await originalSendMessage.apply(this, args);
            
            // Check trial status after sending message
            await checkTrialStatus();
            
            return result;
        };
    }
    
    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
    `;
    document.head.appendChild(style);
    
    // Initialize on page load
    document.addEventListener('DOMContentLoaded', async () => {
        createTrialTimerElement();
        await checkTrialStatus();
        
        if (trialStatus === 'active' && remainingSeconds > 0) {
            startTimer();
        }
        
        // Check trial status every 30 seconds
        setInterval(checkTrialStatus, 30000);
    });
    
    // Export for debugging
    window.trialTimer = {
        checkStatus: checkTrialStatus,
        getStatus: () => ({ status: trialStatus, remaining: remainingSeconds }),
        showPaymentModal: showPaymentRequiredModal
    };
})();