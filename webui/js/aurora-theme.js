import { updateChatInput, sendMessage } from '/index.js';

const promptButtonsSelector = '[data-aria-prompt]';
const intentCardsSelector = '.intent-card';

function handlePrompt(text, autoSend = false) {
  if (!text) return;
  updateChatInput(text);
  const input = document.getElementById('chat-input');
  if (input) {
    input.focus();
  }
  if (autoSend) {
    sendMessage();
  }
}

function hydratePromptButtons() {
  document.querySelectorAll(promptButtonsSelector).forEach((chip) => {
    chip.addEventListener('click', () => {
      const prompt = chip.getAttribute('data-aria-prompt');
      const autoSend = chip.getAttribute('data-aria-send') === 'true';
      handlePrompt(prompt, autoSend);
    });
  });
}

function hydrateIntentCards() {
  document.querySelectorAll(intentCardsSelector).forEach((card) => {
    const prompt = card.getAttribute('data-aria-prompt');
    const autoSend = card.getAttribute('data-aria-send') === 'true';

    card.addEventListener('click', () => handlePrompt(prompt, autoSend));
    card.addEventListener('keypress', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        handlePrompt(prompt, autoSend);
      }
    });
  });
}

function initAuroraTheme() {
  document.body.classList.add('aria-aurora');
  hydratePromptButtons();
  hydrateIntentCards();
}

document.addEventListener('DOMContentLoaded', initAuroraTheme);
