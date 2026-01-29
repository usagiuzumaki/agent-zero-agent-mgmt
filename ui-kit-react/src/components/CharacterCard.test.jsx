import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import CharacterCard from './CharacterCard';

describe('CharacterCard', () => {
  const mockChar = {
    id: '1',
    name: 'John Doe',
    role: 'Protagonist',
    archetype: 'The Hero',
    motivation: 'To save the world',
    bio: 'A brave soul.',
  };

  const mockOnEdit = vi.fn();
  const mockOnDelete = vi.fn();

  it('renders character details correctly', () => {
    render(
      <CharacterCard
        char={mockChar}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
        isDeleting={false}
      />
    );

    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('Protagonist')).toBeInTheDocument();
    expect(screen.getByText('The Hero')).toBeInTheDocument();
    expect(screen.getByText('To save the world')).toBeInTheDocument();
    expect(screen.getByText('A brave soul.')).toBeInTheDocument();
    // Initials check
    expect(screen.getByText('JD')).toBeInTheDocument();
  });

  it('calls onEdit when edit button is clicked', () => {
    render(
      <CharacterCard
        char={mockChar}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
        isDeleting={false}
      />
    );

    const editButton = screen.getByText('Edit');
    fireEvent.click(editButton);
    expect(mockOnEdit).toHaveBeenCalledWith(mockChar);
  });

  it('calls onDelete when delete button is clicked', () => {
    render(
      <CharacterCard
        char={mockChar}
        onEdit={mockOnEdit}
        onDelete={mockOnDelete}
        isDeleting={false}
      />
    );

    const deleteButton = screen.getByText('Delete');
    fireEvent.click(deleteButton);
    expect(mockOnDelete).toHaveBeenCalledWith('1');
  });

  it('disables buttons when isDeleting is true', () => {
    render(
        <CharacterCard
          char={mockChar}
          onEdit={mockOnEdit}
          onDelete={mockOnDelete}
          isDeleting={true}
        />
      );

    const editButton = screen.getByText('Edit');
    // Spinner has aria-label="Loading", so parent button might not be found by text "Delete" if spinner replaces it?
    // Let's check the code: {isDeleting ? <Spinner size="small" /> : 'Delete'}
    // So "Delete" text is gone.
    // We can find by role button that is disabled, or by looking for spinner.
    // The spinner has aria-label="Loading".

    expect(screen.getByLabelText('Loading')).toBeInTheDocument();
    expect(editButton).toBeDisabled();

    // The delete button itself is the parent of the spinner.
    // We can find it by getting the parent of the spinner or querying all buttons.
    const buttons = screen.getAllByRole('button');
    expect(buttons[1]).toBeDisabled(); // usually the second button
  });
});
