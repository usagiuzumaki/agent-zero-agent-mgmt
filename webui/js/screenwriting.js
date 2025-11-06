/**
 * Screenwriting Tools Dropdown Menu
 * Provides quick access to screenwriting features like book outlines, story bibles, 
 * character profiles, quotes, and sketches with imagery
 */

(function() {
    // Screenwriting tools configuration
    const screenwritingTools = [
        {
            id: 'book_outline',
            icon: '📚',
            label: 'Book Outline',
            prompt: 'Show me the current book outline and structure. Include chapters, scenes, and plot progression.',
            description: 'View and edit your book structure'
        },
        {
            id: 'story_bible',
            icon: '📖',
            label: 'Story Bible',
            prompt: 'Display the story bible with world-building details, lore, rules, and universe guidelines.',
            description: 'Access world-building and lore'
        },
        {
            id: 'character_profiles', 
            icon: '👥',
            label: 'Character Profiles',
            prompt: 'Show me all character profiles with their backstories, motivations, and development arcs. Include visual references if available.',
            description: 'Manage character development'
        },
        {
            id: 'sick_quotes',
            icon: '✍️',
            label: 'Sick Quotes',
            prompt: 'Display all the memorable quotes and dialogue we\'ve written so far. Group them by character or scene.',
            description: 'Collection of powerful dialogue'
        },
        {
            id: 'sketches_imagery',
            icon: '🎨',
            label: 'Sketches & Imagery',
            prompt: 'Show me all visual sketches, scene imagery, and concept art we\'ve created. Include mood boards and visual references.',
            description: 'Visual concepts and artwork'
        },
        {
            id: 'scene_generator',
            icon: '🎬',
            label: 'Scene Generator',
            prompt: 'Let\'s write a new scene. Ask me which characters, setting, and conflict to focus on.',
            description: 'Create new scenes'
        },
        {
            id: 'dialogue_workshop',
            icon: '💬',
            label: 'Dialogue Workshop',
            prompt: 'Help me craft authentic dialogue. Let\'s work on character voice and subtext.',
            description: 'Refine character dialogue'
        },
        {
            id: 'plot_analyzer',
            icon: '📊',
            label: 'Plot Analyzer',
            prompt: 'Analyze the current plot structure for pacing, tension, and story beats. Identify any plot holes or weak areas.',
            description: 'Story structure analysis'
        }
    ];

    // Create dropdown HTML
    function createScreenwritingDropdownHTML() {
        return `
            <div class="screenwriting-dropdown-container">
                <button class="text-button screenwriting-toggle" onclick="window.screenwriting.toggleDropdown()">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 2L2 7L12 12L22 7L12 2Z"></path>
                        <path d="M2 17L12 22L22 17"></path>
                        <path d="M2 12L12 17L22 12"></path>
                    </svg>
                    <span>Screenwriting</span>
                </button>
                <div id="screenwriting-dropdown" class="screenwriting-dropdown hidden">
                    ${screenwritingTools.map(tool => `
                        <div class="screenwriting-item" onclick="window.screenwriting.selectTool('${tool.id}')">
                            <span class="screenwriting-icon">${tool.icon}</span>
                            <div class="screenwriting-content">
                                <span class="screenwriting-label">${tool.label}</span>
                                <span class="screenwriting-description">${tool.description}</span>
                            </div>
                        </div>
                    `).join('')}
                    <div class="screenwriting-divider"></div>
                    <div class="screenwriting-item" onclick="window.screenwriting.newProject()">
                        <span class="screenwriting-icon">✨</span>
                        <div class="screenwriting-content">
                            <span class="screenwriting-label">New Project</span>
                            <span class="screenwriting-description">Start a fresh screenplay</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Toggle dropdown visibility
    function toggleDropdown() {
        const dropdown = document.getElementById('screenwriting-dropdown');
        if (dropdown) {
            dropdown.classList.toggle('hidden');
            
            // Close activities dropdown if open
            const activitiesDropdown = document.getElementById('activities-dropdown');
            if (activitiesDropdown && !activitiesDropdown.classList.contains('hidden')) {
                activitiesDropdown.classList.add('hidden');
            }
        }
    }

    // Handle tool selection
    function selectTool(toolId) {
        const tool = screenwritingTools.find(t => t.id === toolId);
        if (tool) {
            // Fill the input with the tool's prompt
            const input = document.getElementById('user-input');
            if (input) {
                input.value = tool.prompt;
                input.focus();
                
                // Trigger input event to update Alpine data
                const event = new Event('input', { bubbles: true });
                input.dispatchEvent(event);
            }
            
            // Log the selection
            console.log(`[Screenwriting] Selected: ${tool.icon} ${tool.label}`);
            
            // Close dropdown
            toggleDropdown();
            
            // Store last used tool in localStorage
            localStorage.setItem('lastScreenwritingTool', toolId);
        }
    }

    // Create new project
    function newProject() {
        const input = document.getElementById('user-input');
        if (input) {
            input.value = 'Let\'s start a new screenwriting project! What genre are we working with? What\'s the basic premise or logline?';
            input.focus();
            
            // Trigger input event
            const event = new Event('input', { bubbles: true });
            input.dispatchEvent(event);
        }
        
        console.log('[Screenwriting] Starting new project');
        toggleDropdown();
    }

    // Load saved data (for future persistent storage)
    async function loadScreenwritingData(type) {
        try {
            const response = await fetch(`/api/screenwriting/${type}`);
            if (response.ok) {
                const data = await response.json();
                return data;
            }
        } catch (error) {
            console.error(`Error loading ${type}:`, error);
        }
        return null;
    }

    // Save data (for future persistent storage)
    async function saveScreenwritingData(type, data) {
        try {
            const response = await fetch(`/api/screenwriting/${type}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (response.ok) {
                console.log(`[Screenwriting] Saved ${type}`);
                return true;
            }
        } catch (error) {
            console.error(`Error saving ${type}:`, error);
        }
        return false;
    }

    // Quick actions for common tasks
    function quickAction(action) {
        const quickActions = {
            'new_character': 'Create a new character profile. Let me know their name, role in the story, and key personality traits.',
            'new_scene': 'Write a new scene. What\'s the setting, who\'s involved, and what\'s the conflict?',
            'new_quote': 'Add a memorable quote or piece of dialogue. Which character says it and in what context?',
            'generate_image': 'Generate concept art or a visual sketch. Describe the scene, character, or mood you want to capture.'
        };

        const prompt = quickActions[action];
        if (prompt) {
            const input = document.getElementById('user-input');
            if (input) {
                input.value = prompt;
                input.focus();
                const event = new Event('input', { bubbles: true });
                input.dispatchEvent(event);
            }
        }
    }

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('[Screenwriting] Initializing screenwriting tools');
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(event) {
            const dropdown = document.getElementById('screenwriting-dropdown');
            const button = document.querySelector('.screenwriting-toggle');
            
            if (dropdown && button && !dropdown.contains(event.target) && !button.contains(event.target)) {
                dropdown.classList.add('hidden');
            }
        });
    });

    // Export functions to global scope
    window.screenwriting = {
        createDropdownHTML: createScreenwritingDropdownHTML,
        toggleDropdown: toggleDropdown,
        selectTool: selectTool,
        newProject: newProject,
        loadData: loadScreenwritingData,
        saveData: saveScreenwritingData,
        quickAction: quickAction,
        tools: screenwritingTools
    };
})();