// Supabase-backed Auth JavaScript Integration

(function() {
    'use strict';
    
    // Check auth status on page load
    document.addEventListener('DOMContentLoaded', async function() {
        await checkAuthStatus();
    });
    
    async function checkAuthStatus() {
        const authContainer = document.getElementById('auth-container');
        if (!authContainer) return;
        
        try {
            // Check if user is authenticated
            const response = await fetch('/auth/user', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'same-origin'
            });
            
            if (response.ok) {
                const userData = await response.json();
                if (userData.authenticated) {
                    // User is logged in
                    displayUserProfile(userData);
                } else {
                    // User is not logged in
                    displayLoginButton();
                }
            } else {
                // Auth not available or error
                displayLoginButton();
            }
        } catch (error) {
            console.log('Auth check failed:', error);
            displayLoginButton();
        }
    }
    
    function displayLoginButton() {
        const authContainer = document.getElementById('auth-container');
        authContainer.innerHTML = `
            <a href="/auth/login" class="auth-btn">
                <i class="fas fa-sign-in-alt"></i> Sign In
            </a>
        `;
    }
    
    function displayUserProfile(userData) {
        const authContainer = document.getElementById('auth-container');
        const profileImageUrl = userData.profile_image_url || '/public/default-avatar.svg';
        const displayName = userData.first_name || userData.email || 'User';
        
        authContainer.innerHTML = `
            <div class="user-profile">
                <img src="${profileImageUrl}" alt="${displayName}" class="user-avatar" onerror="this.src='/public/default-avatar.svg'">
                <span class="user-name">${displayName}</span>
                <button onclick="logout()" class="logout-btn">
                    <i class="fas fa-sign-out-alt"></i> Logout
                </button>
            </div>
        `;
        
        // Show auth success message
        showAuthStatus('Welcome back, ' + displayName + '!');
    }
    
    window.logout = async function() {
        try {
            await fetch('/auth/logout', {
                method: 'GET',
                credentials: 'same-origin'
            });
            
            // Reload page to update UI
            window.location.reload();
        } catch (error) {
            console.error('Logout failed:', error);
        }
    }
    
    function showAuthStatus(message) {
        const statusEl = document.createElement('div');
        statusEl.className = 'auth-status show';
        statusEl.textContent = message;
        document.body.appendChild(statusEl);
        
        setTimeout(() => {
            statusEl.remove();
        }, 3000);
    }
    
    // Export for use in other scripts
    window.checkAuthStatus = checkAuthStatus;
    window.showAuthStatus = showAuthStatus;
})();