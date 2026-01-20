import React, { useState, useEffect } from 'react';
import Spinner from './common/Spinner';
import './StorybookUI.css';

export default function StorybookUI() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [uploadContent, setUploadContent] = useState('');
  const [uploadName, setUploadName] = useState('');
  const [showUpload, setShowUpload] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [deletingId, setDeletingId] = useState(null);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/screenwriting/storybook');
      if (!response.ok) {
        throw new Error('Failed to fetch storybook data');
      }
      const data = await response.json();
      if (data && data.documents) {
        setDocuments(data.documents);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!uploadContent.trim()) return;
    setIsUploading(true);
    setError(null);

    try {
      const response = await fetch('/api/screenwriting/storybook/upload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: uploadName || 'Untitled Document',
          content: uploadContent,
          description: 'Uploaded via StorybookUI'
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to upload document');
      }

      await fetchDocuments();
      setShowUpload(false);
      setUploadName('');
      setUploadContent('');
    } catch (err) {
      setError(err.message);
    } finally {
      setIsUploading(false);
    }
  };

  const handleDelete = async (docId) => {
    if (!window.confirm("Are you sure you want to delete this document? This cannot be undone.")) return;

    setDeletingId(docId);
    try {
      const response = await fetch('/api/screenwriting/storybook/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: docId })
      });

      if (!response.ok) {
        throw new Error('Failed to delete document');
      }

      await fetchDocuments();
    } catch (err) {
      setError(err.message);
    } finally {
      setDeletingId(null);
    }
  };

  const calculateTensionColor = (beatIndex, totalBeats) => {
    // Simple visualizer: start low, rise, dip, rise high
    const progress = beatIndex / totalBeats;
    if (progress < 0.25) return 'var(--color-tension-low)';
    if (progress < 0.5) return 'var(--color-tension-med)';
    if (progress < 0.75) return 'var(--color-tension-high)';
    return 'var(--color-tension-climax)';
  };

  if (loading && !documents.length) {
    return (
      <div className="storybook-ui loading-container">
         <Spinner size="large" />
         <p>Loading Storybook...</p>
      </div>
    );
  }

  return (
    <div className="storybook-ui">
      <div className="storybook-header">
        <h3>Storybook</h3>
        <button
          className="btn-secondary"
          onClick={() => setShowUpload(!showUpload)}
          aria-expanded={showUpload}
          aria-controls="upload-panel"
        >
          {showUpload ? 'Cancel' : 'New Document'}
        </button>
      </div>

      {error && (
        <div className="error-message" role="alert">
          <span>{error}</span>
          <button className="btn-close-error" onClick={() => setError(null)} aria-label="Dismiss error">×</button>
        </div>
      )}

      {showUpload && (
        <div id="upload-panel" className="storybook-upload">
          <h4>Ingest New Document</h4>
          <form onSubmit={handleUpload}>
            <label htmlFor="doc-title" className="input-label">Document Title</label>
            <input
              id="doc-title"
              type="text"
              placeholder="e.g. My Screenplay Draft"
              value={uploadName}
              onChange={(e) => setUploadName(e.target.value)}
              className="input-field"
            />
            <label htmlFor="doc-content" className="input-label">Paste Text Content</label>
            <textarea
              id="doc-content"
              placeholder="Paste text content here to generate beats..."
              value={uploadContent}
              onChange={(e) => setUploadContent(e.target.value)}
              className="textarea-field"
              rows={10}
            />
            <div className="form-actions">
              <button type="submit" className="btn-primary" disabled={isUploading || !uploadContent.trim()}>
                {isUploading ? (
                  <span className="flex-center gap-2">
                    <Spinner size="small" color="white" /> Ingesting...
                  </span>
                ) : 'Ingest Document'}
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="storybook-content">
        {!selectedDoc ? (
          <div className="document-list">
            {documents.length === 0 ? (
              <div className="empty-state-container">
                <div className="empty-state-icon">
                  <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                    <path d="M12 6.25278V19.2528M12 6.25278C10.8321 5.4392 9.24649 5 7.5 5C5.75351 5 4.16789 5.4392 3 6.25278V19.2528C4.16789 18.4392 5.75351 18 7.5 18C9.24649 18 10.8321 18.4392 12 19.2528M12 6.25278C13.1679 5.4392 14.7535 5 16.5 5C18.2465 5 19.8321 5.4392 21 6.25278V19.2528C19.8321 18.4392 18.2465 18 16.5 18C14.7535 18 13.1679 18.4392 12 19.2528" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
                <h3 className="empty-state-title">No Storybooks Yet</h3>
                <p className="empty-state-text">Create your first screenwriting document to begin your journey.</p>
                <button
                  className="btn-primary btn-empty-state"
                  onClick={() => setShowUpload(true)}
                >
                  Create First Document
                </button>
              </div>
            ) : (
              documents.map((doc) => (
                <div key={doc.id} className="document-card">
                  <button
                    className="document-content-clickable"
                    onClick={() => setSelectedDoc(doc)}
                    type="button"
                  >
                    <h4>{doc.name}</h4>
                    <p>{doc.description}</p>
                    <span className="doc-meta">Uploaded: {new Date(doc.uploaded_at).toLocaleDateString()}</span>
                    <div className="tags">
                      {doc.tags.map((tag, i) => <span key={i} className="tag">{tag}</span>)}
                    </div>
                  </button>
                  <div className="doc-actions">
                    <button
                      className="btn-icon delete-doc-btn"
                      onClick={() => handleDelete(doc.id)}
                      aria-label={`Delete ${doc.name}`}
                      title="Delete Document"
                      disabled={deletingId === doc.id}
                    >
                      {deletingId === doc.id ? (
                        <Spinner size="small" />
                      ) : (
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                          <path d="M4 7H20" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                          <path d="M10 11V17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                          <path d="M14 11V17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                          <path d="M5 7L6 19C6 20.1046 6.89543 21 8 21H16C17.1046 21 18 20.1046 18 19L19 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                          <path d="M9 7V4C9 3.44772 9.44772 3 10 3H14C14.5523 3 15 3.44772 15 4V7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                      )}
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        ) : (
          <div className="document-view">
            <button className="btn-back" onClick={() => setSelectedDoc(null)}>← Back to List</button>
            <div className="doc-header">
              <h3>{selectedDoc.name}</h3>
              {selectedDoc.suggestions && selectedDoc.suggestions.length > 0 && (
                <div className="doc-suggestions">
                  <strong>AI Suggestions:</strong>
                  <ul>
                    {selectedDoc.suggestions.map((s, i) => <li key={i}>{s}</li>)}
                  </ul>
                </div>
              )}
            </div>

            <div className="chapters-list">
              {selectedDoc.chapters.map((chapter, cIndex) => (
                <div key={chapter.id} className="chapter-item">
                  <div className="chapter-header-row">
                    <h5>{chapter.title}</h5>
                    <span className="structure-tag">Act {cIndex + 1}</span>
                  </div>
                  <p className="chapter-summary">{chapter.summary}</p>

                  <div className="beats-timeline" aria-hidden="true">
                     {/* Visual Timeline Bar */}
                     <div className="timeline-track">
                       {chapter.beats.map((beat, i) => (
                         <div
                           key={i}
                           className="timeline-dot"
                           style={{
                             left: `${(i / (chapter.beats.length - 1 || 1)) * 100}%`,
                             backgroundColor: calculateTensionColor(i, chapter.beats.length)
                           }}
                           title={beat.label}
                         />
                       ))}
                     </div>
                  </div>

                  <div className="beats-grid">
                    {chapter.beats.map((beat, bIndex) => (
                      <div
                        key={beat.id}
                        className="beat-card"
                        style={{borderLeft: `3px solid ${calculateTensionColor(bIndex, chapter.beats.length)}`}}
                      >
                        <div className="beat-header">
                          <span className="beat-label">{beat.label}</span>
                          <button
                            className="btn-icon"
                            title="Draft Dialogue"
                            aria-label={`Draft Dialogue for ${beat.label}`}
                          >
                            📝
                          </button>
                        </div>
                        <p>{beat.summary}</p>
                        <small className="visual-prompt">🎨 {beat.visual_prompt}</small>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
