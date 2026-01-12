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

  const handleDelete = async (e, docId) => {
    e.stopPropagation();
    if (!window.confirm('Are you sure you want to delete this document?')) return;

    try {
      const response = await fetch('/api/screenwriting/storybook/delete', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: docId }),
      });

      if (!response.ok) {
        throw new Error('Failed to delete document');
      }

      await fetchDocuments();
    } catch (err) {
      setError(err.message);
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
        <div className="modal-overlay" onClick={() => setShowUpload(false)}>
          <div
            id="upload-panel"
            className="storybook-upload-modal"
            onClick={(e) => e.stopPropagation()}
            role="dialog"
            aria-modal="true"
            aria-labelledby="upload-title"
          >
            <h4 id="upload-title">Ingest New Document</h4>
            <form onSubmit={handleUpload}>
              <label htmlFor="doc-title" className="input-label">Document Title</label>
              <input
                id="doc-title"
                type="text"
                placeholder="e.g. My Screenplay Draft"
                value={uploadName}
                onChange={(e) => setUploadName(e.target.value)}
                className="input-field"
                autoFocus
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
                <button
                   type="button"
                   className="btn-secondary"
                   onClick={() => setShowUpload(false)}
                   disabled={isUploading}
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary" disabled={isUploading}>
                  {isUploading ? (
                    <span className="flex-center gap-2">
                      <Spinner size="small" color="white" /> Ingesting...
                    </span>
                  ) : 'Ingest Document'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="storybook-content">
        {!selectedDoc ? (
          <div className="document-list">
            {documents.length === 0 ? (
              <p className="empty-state">No documents found. Upload one to get started.</p>
            ) : (
              documents.map((doc) => (
                <div
                  key={doc.id}
                  className="document-card"
                  onClick={() => setSelectedDoc(doc)}
                  role="button"
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      setSelectedDoc(doc);
                    }
                  }}
                >
                  <div className="doc-card-header">
                    <h4>{doc.name}</h4>
                    <button
                      className="btn-icon delete-btn"
                      onClick={(e) => handleDelete(e, doc.id)}
                      title="Delete Document"
                      aria-label={`Delete ${doc.name}`}
                    >
                      🗑️
                    </button>
                  </div>
                  <p>{doc.description}</p>
                  <span className="doc-meta">Uploaded: {new Date(doc.uploaded_at).toLocaleDateString()}</span>
                  <div className="tags">
                    {doc.tags.map((tag, i) => <span key={i} className="tag">{tag}</span>)}
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
