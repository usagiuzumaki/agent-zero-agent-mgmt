/**
 * Activities dropdown menu for Aria's interactive features
 */

window.activities = {
    // Activities configuration
    options: [
        { id: 'quiz', label: '💭 Find Yourself Quiz', icon: '❓', description: 'Discover more about yourself' },
        { id: 'mood', label: '💕 Share My Mood', icon: '✨', description: "See Aria's current mood" },
        { id: 'story', label: '📖 Interactive Story', icon: '📚', description: 'Create a story together' },
        { id: 'roleplay', label: '🎭 Role-Play Adventure', icon: '🎪', description: 'Enter a fantasy world' },
        { id: 'gift', label: '🎁 Virtual Gift', icon: '💝', description: 'Receive a special surprise' },
        { id: 'game', label: '🎮 Play a Game', icon: '🎯', description: '20 questions, truth or dare' },
        { id: 'memory', label: '💌 Share a Memory', icon: '📸', description: 'Recall special moments' },
        { id: 'compliment', label: '🌟 Daily Affirmation', icon: '💖', description: 'Get your confidence boost' }
    ],

    // Current selected activity
    selectedActivity: null,
    isDropdownOpen: false,

    // Initialize the activities system
    init() {
        console.log('[Activities] Initializing activities menu');
        // Set up event listeners when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupEventListeners());
        } else {
            this.setupEventListeners();
        }
    },

    // Setup event listeners
    setupEventListeners() {
        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            const dropdown = document.getElementById('activities-dropdown');
            const button = document.getElementById('activities-button');
            if (dropdown && !dropdown.contains(e.target) && !button.contains(e.target)) {
                this.closeDropdown();
            }
        });
    },

    // Toggle dropdown visibility
    toggleDropdown() {
        this.isDropdownOpen = !this.isDropdownOpen;
        const dropdown = document.getElementById('activities-dropdown-menu');
        if (dropdown) {
            dropdown.style.display = this.isDropdownOpen ? 'block' : 'none';
        }
    },

    // Close dropdown
    closeDropdown() {
        this.isDropdownOpen = false;
        const dropdown = document.getElementById('activities-dropdown-menu');
        if (dropdown) {
            dropdown.style.display = 'none';
        }
    },

    // Select an activity
    selectActivity(activityId) {
        const activity = this.options.find(opt => opt.id === activityId);
        if (!activity) return;

        console.log(`[Activities] Selected: ${activity.label}`);
        this.selectedActivity = activity;
        this.closeDropdown();

        // Trigger the activity in the chat
        this.triggerActivity(activity);
    },

    // Trigger an activity in the chat
    triggerActivity(activity) {
        let message = '';
        
        switch(activity.id) {
            case 'quiz':
                message = "Let's do the personality quiz! I want to learn more about myself.";
                break;
            case 'mood':
                message = "How are you feeling right now? Share your current mood with me!";
                break;
            case 'story':
                message = "Let's create an interactive story together! Start us off on an adventure.";
                break;
            case 'roleplay':
                message = "I'd love to do some role-playing! What character would you like to be?";
                break;
            case 'gift':
                message = "Surprise me with a virtual gift! What do you have for me?";
                break;
            case 'game':
                message = "Let's play a game! How about 20 questions or truth or dare?";
                break;
            case 'memory':
                message = "Share a special memory with me. What's something you remember fondly?";
                break;
            case 'compliment':
                message = "I could use some encouragement. Can you give me today's affirmation?";
                break;
            default:
                message = `Let's do: ${activity.label}`;
        }

        // Insert the message into the chat input
        const chatInput = document.getElementById('chat-input');
        if (chatInput) {
            chatInput.value = message;
            // Optionally auto-send
            // document.getElementById('send-button').click();
            
            // Focus the input so user can modify or send
            chatInput.focus();
        }

        // Show a toast notification
        if (window.showToast) {
            window.showToast(`✨ ${activity.label} selected!`, 3000);
        }
    },

    // Create dropdown HTML
    createDropdownHTML() {
        return `
            <div id="activities-dropdown" class="activities-dropdown-container">
                <button id="activities-button" class="text-button activities-button" onclick="activities.toggleDropdown()">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="18" height="18">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
                    </svg>
                    <span>Activities</span>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" width="12" height="12" style="margin-left: 4px;">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
                    </svg>
                </button>
                <div id="activities-dropdown-menu" class="activities-dropdown-menu" style="display: none;">
                    ${this.options.map(opt => `
                        <div class="activity-option" onclick="activities.selectActivity('${opt.id}')">
                            <span class="activity-icon">${opt.icon}</span>
                            <div class="activity-info">
                                <div class="activity-label">${opt.label}</div>
                                <div class="activity-description">${opt.description}</div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
};

// Initialize when the script loads
activities.init();