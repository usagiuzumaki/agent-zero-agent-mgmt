import React, { useState, useEffect } from 'react';
import Spinner from './common/Spinner';
import EmptyState from './common/EmptyState';
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
    if (progress < 0.25) return '#60a5fa'; // Blue
    if (progress < 0.5) return '#fbbf24'; // Amber
    if (progress < 0.75) return '#f87171'; // Red-400
    return '#ef4444'; // Red-500
  };

  if (loading && !documents.length) {
    return (
      <div className="loading-container">
         <Spinner size="large" />
         <p style={{marginTop: '1rem'}}>Loading Storybook...</p>
      </div>
    );
  }

  return (
    <div className="storybook-ui">
      {!selectedDoc && (
        <div className="storybook-header">
            <h3>Storybook Documents</h3>
            <button
            className="btn-studio-primary"
            onClick={() => setShowUpload(!showUpload)}
            >
            {showUpload ? 'Cancel' : '+ New Document'}
            </button>
        </div>
      )}

      {error && (
        <div className="error-message" role="alert">
          <span>{error}</span>
          <button className="btn-close-error" onClick={() => setError(null)}>×</button>
        </div>
      )}

      {showUpload && (
        <div className="storybook-upload">
          <h4>Ingest New Document</h4>
          <form onSubmit={handleUpload}>
            <label className="input-label">Document Title</label>
            <input
              type="text"
              placeholder="e.g. My Screenplay Draft"
              value={uploadName}
              onChange={(e) => setUploadName(e.target.value)}
              className="input-field"
              autoFocus
            />
            <label className="input-label">Paste Text Content</label>
            <textarea
              placeholder="Paste text content here to generate beats..."
              value={uploadContent}
              onChange={(e) => setUploadContent(e.target.value)}
              className="textarea-field"
              rows={10}
            />
            <div className="form-actions">
              <button type="submit" className="btn-studio-primary" disabled={isUploading || !uploadContent.trim()}>
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
              <EmptyState
                icon={<span>📖</span>}
                description="No documents found. Start your story by creating or uploading a new document."
                action={
                  <button
                    className="btn-studio-primary"
                    onClick={() => setShowUpload(true)}
                  >
                    Create First Document
                  </button>
                }
              />
            ) : (
              documents.map((doc) => (
                <div key={doc.id} className="document-card">
                  <button
                    className="document-content-clickable"
                    onClick={() => setSelectedDoc(doc)}
                    type="button"
                  >
                    <h4>{doc.name}</h4>
                    <p>{doc.description || 'No description'}</p>
                    <span className="doc-meta">Uploaded: {new Date(doc.uploaded_at).toLocaleDateString()}</span>
                    <div className="tags">
                      {doc.tags && doc.tags.map((tag, i) => <span key={i} className="tag">{tag}</span>)}
                    </div>
                  </button>
                  <div className="doc-actions">
                    <button
                      className="btn-icon delete-doc-btn"
                      onClick={() => handleDelete(doc.id)}
                      title="Delete Document"
                      disabled={deletingId === doc.id}
                    >
                      {deletingId === doc.id ? (
                        <Spinner size="small" />
                      ) : (
                        <span>🗑️</span>
                      )}
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        ) : (
          <div className="document-view">
             <div className="doc-header-row">
                <button className="btn-back" onClick={() => setSelectedDoc(null)}>
                    <span>←</span> Back to Library
                </button>
                <h3 style={{margin:0}}>{selectedDoc.name}</h3>
                <div style={{width: 60}}></div> {/* Spacer */}
            </div>

            <div className="chapters-container">
              {selectedDoc.chapters.map((chapter, cIndex) => (
                <div key={chapter.id} className="chapter-section">
                  <div className="chapter-title">
                     <span className="act-badge">Act {cIndex + 1}</span>
                     <span>{chapter.title}</span>
                  </div>

                  <div className="beats-scroller">
                    {chapter.beats.map((beat, bIndex) => (
                      <div
                        key={beat.id}
                        className="beat-card"
                        style={{borderTopColor: calculateTensionColor(bIndex, chapter.beats.length)}}
                      >
                        <div className="beat-card-header">
                            <span className="beat-type" style={{color: calculateTensionColor(bIndex, chapter.beats.length)}}>
                                {beat.label}
                            </span>
                            <span className="visual-hint" title={beat.visual_prompt}>
                                {bIndex % 2 === 0 ? '🎬' : '👁️'}
                            </span>
                        </div>
                        <div className="beat-content">
                            {beat.summary}
                        </div>
                        <div className="beat-footer">
                             <button className="btn-draft">
                                ✍️ Draft Scene
                             </button>
                        </div>
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
