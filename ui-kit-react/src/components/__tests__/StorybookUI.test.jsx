import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import StorybookUI from '../StorybookUI';

describe('StorybookUI', () => {
  beforeEach(() => {
    // Reset mocks before each test
    global.fetch = vi.fn();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('shows loading state initially', async () => {
    // Mock a pending promise to keep it in loading state
    global.fetch.mockImplementation(() => new Promise(() => {}));

    render(<StorybookUI />);

    expect(screen.getByText(/Loading Storybook/i)).toBeInTheDocument();
  });

  it('shows empty state when no documents are returned', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ documents: [] }),
    });

    render(<StorybookUI />);

    await waitFor(() => {
        expect(screen.queryByText(/Loading Storybook/i)).not.toBeInTheDocument();
    });

    expect(screen.getByText(/No documents found/i)).toBeInTheDocument();
    expect(screen.getByText(/Create First Document/i)).toBeInTheDocument();
  });

  it('renders a list of documents when fetched successfully', async () => {
    const mockDocs = [
      { id: '1', name: 'Script Alpha', description: 'A test script', uploaded_at: new Date().toISOString(), tags: ['sci-fi'] },
      { id: '2', name: 'Script Beta', description: 'Another script', uploaded_at: new Date().toISOString(), tags: ['drama'] },
    ];

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ documents: mockDocs }),
    });

    render(<StorybookUI />);

    await waitFor(() => {
      expect(screen.getByText('Script Alpha')).toBeInTheDocument();
    });

    expect(screen.getByText('Script Beta')).toBeInTheDocument();
    expect(screen.getByText('A test script')).toBeInTheDocument();
  });

  it('shows error message when fetch fails', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
    });

    render(<StorybookUI />);

    await waitFor(() => {
      expect(screen.getByText(/Failed to fetch storybook data/i)).toBeInTheDocument();
    });
  });

  it('opens upload form when "Create First Document" is clicked', async () => {
     global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ documents: [] }),
    });

    render(<StorybookUI />);

    await waitFor(() => {
        expect(screen.getByText(/Create First Document/i)).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText(/Create First Document/i));

    expect(screen.getByText(/Ingest New Document/i)).toBeInTheDocument();
  });
});
