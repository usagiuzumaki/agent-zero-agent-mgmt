import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import EmptyState from './EmptyState';

describe('EmptyState', () => {
  it('renders title and description', () => {
    render(<EmptyState title="Test Title" description="Test Description" />);
    expect(screen.getByText('Test Title')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
  });

  it('renders action if provided', () => {
    render(<EmptyState title="Test Title" action={<button>Click Me</button>} />);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('renders nothing if no props provided', () => {
      const { container } = render(<EmptyState />);
      // It renders the container div but empty inside mostly
      expect(container.firstChild).toHaveClass('empty-state-container');
  });
});
