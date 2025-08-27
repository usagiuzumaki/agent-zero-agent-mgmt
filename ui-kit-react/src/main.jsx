import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import './theme.css';
import App from './App.jsx';
import { registerTool } from './plugins';

// Example plugin tool
registerTool({
  name: 'greet',
  label: 'Greet',
  action: (cb) => cb('Hello from plugin!'),
});

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
);
