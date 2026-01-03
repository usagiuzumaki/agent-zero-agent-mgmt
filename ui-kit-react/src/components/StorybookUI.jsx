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

  const calculateTensionColor = (beatIndex, totalBeats) => {
    // Simple visualizer: start low, rise, dip, rise high
    const progress = beatIndex / totalBeats;
    if (progress < 0.25) return '#60a5fa'; // Blue (setup)
    if (progress < 0.5) return '#fbbf24';  // Yellow (rising)
    if (progress < 0.75) return '#f87171'; // Red (climax approach)
    return '#ef4444'; // Dark Red (Climax)
  };

  if (loading && !documents.length) return <div className="loading">Loading Storybook...</div>;

  return (
    <div className="storybook-ui">
      <div className="storybook-header">
        <h3>Storybook</h3>
        <button className="btn-secondary" onClick={() => setShowUpload(!showUpload)}>
          {showUpload ? 'Cancel' : 'New Document'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {showUpload && (
        <div className="storybook-upload">
          <h4>Ingest New Document</h4>
          <form onSubmit={handleUpload}>
            <label htmlFor="doc-title" className="sr-only">Document Title</label>
            <input
              id="doc-title"
              type="text"
              placeholder="Document Title"
              value={uploadName}
              onChange={(e) => setUploadName(e.target.value)}
              className="input-field"
            />
            <label htmlFor="doc-content" className="sr-only">Document Content</label>
            <textarea
              id="doc-content"
              placeholder="Paste text content here..."
              value={uploadContent}
              onChange={(e) => setUploadContent(e.target.value)}
              className="textarea-field"
              rows={10}
            />
            <button type="submit" className="btn-primary" disabled={isUploading}>
              {isUploading ? (
                <>
                  <Spinner size="small" color="#fff" />
                  <span>Ingesting...</span>
                </>
              ) : (
                'Ingest'
              )}
            </button>
          </form>
        </div>
      )}

      <div className="storybook-content">
        {!selectedDoc ? (
          <div className="document-list">
            {documents.length === 0 ? (
              <p className="empty-state">No documents found. Upload one to get started.</p>
            ) : (
              documents.map((doc) => (
                <button
                  key={doc.id}
                  className="document-card"
                  onClick={() => setSelectedDoc(doc)}
                  type="button"
                >
                  <h4>{doc.name}</h4>
                  <p>{doc.description}</p>
                  <span className="doc-meta">{new Date(doc.uploaded_at).toLocaleDateString()}</span>
                  <div className="tags">
                    {doc.tags.map((tag, i) => <span key={i} className="tag">{tag}</span>)}
                  </div>
                </button>
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

                  <div className="beats-timeline">
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
                            aria-label="Draft Dialogue"
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
