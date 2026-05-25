import { useState, useEffect } from 'react'
import axios from 'axios'

interface Meeting {
  id: string
  title: string
  status: string
  created_at: string
  summary?: string
  transcript?: string
  action_items?: string
}

export default function App() {
  const [meetings, setMeetings] = useState<Meeting[]>([])
  const [selectedMeeting, setSelectedMeeting] = useState<Meeting | null>(null)
  const [title, setTitle] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState('')
  const [darkMode, setDarkMode] = useState(false)
  const [files, setFiles] = useState<File[]>([])

  useEffect(() => {
    loadMeetings()
  }, [])

  const loadMeetings = async () => {
    try {
      const res = await axios.get('/api/v1/meetings')
      setMeetings(res.data)
    } catch (err) {
      console.error('Error loading meetings:', err)
    }
  }

const handleUpload = async (e: React.FormEvent) => {
  e.preventDefault()
  if (files.length === 0 || !title) {
    setStatus('Please select files and add title')
    return
  }

  setLoading(true)
  try {
    let uploadedCount = 0
    
    // Upload each file
    for (let i = 0; i < files.length; i++) {
      const file = files[i]
      const formData = new FormData()
      formData.append('title', `${title} (Part ${i + 1}/${files.length})`)
      formData.append('audio_file', file)

      const res = await axios.post('/api/v1/meetings', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      
      uploadedCount++
      setStatus(`Uploaded ${uploadedCount}/${files.length} files...`)
    }

    setStatus(`All ${uploadedCount} files uploaded! Processing...`)
    setTitle('')
    setFiles([])
    loadMeetings()

    // Poll for updates every 2 seconds for 2 minutes
    const pollInterval = setInterval(() => {
      loadMeetings()
    }, 2000)

    setTimeout(() => clearInterval(pollInterval), 120000)
    
  } catch (err: any) {
    setStatus('Error: ' + (err.response?.data?.detail || err.message))
  } finally {
    setLoading(false)
  }
}

  const handleSelectMeeting = async (meeting: Meeting) => {
    try {
      const res = await axios.get(`/api/v1/meetings/${meeting.id}`)
      setSelectedMeeting(res.data)
    } catch (err) {
      console.error('Error loading meeting:', err)
    }
  }

  // Detail View
if (selectedMeeting) {
    return (
      <div style={{ 
        maxWidth: '900px', 
        margin: '0 auto', 
        padding: '20px', 
        fontFamily: 'Arial',
        backgroundColor: darkMode ? '#1a1a1a' : '#ffffff',
        color: darkMode ? '#ffffff' : '#000000',
        minHeight: '100vh',
        transition: 'all 0.3s ease'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <button onClick={() => setSelectedMeeting(null)} style={{ padding: '10px 20px' }}>
            ← Back to Meetings
          </button>
          <button 
            onClick={() => setDarkMode(!darkMode)}
            style={{ padding: '10px 15px', fontSize: '20px', cursor: 'pointer', border: 'none', borderRadius: '5px', backgroundColor: darkMode ? '#333' : '#eee' }}
          >
            {darkMode ? '☀️' : '🌙'}
          </button>
        </div>

        <h1>{selectedMeeting.title}</h1>
        <p>Status: <strong>{selectedMeeting.status}</strong></p>
        <p>{new Date(selectedMeeting.created_at).toLocaleString()}</p>

       {selectedMeeting.status === 'completed' ? (
  <>
    {/* Export Buttons */}
    <div style={{ marginTop: '20px', marginBottom: '20px', display: 'flex', gap: '10px' }}>
      <button 
        onClick={async () => {
          const res = await axios.get(`/api/v1/meetings/${selectedMeeting.id}/export/markdown`)
          const element = document.createElement('a')
          element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(res.data.content))
          element.setAttribute('download', res.data.filename)
          element.style.display = 'none'
          document.body.appendChild(element)
          element.click()
          document.body.removeChild(element)
        }}
        style={{ padding: '10px 20px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
      >
        📝 Download Markdown
      </button>
      
      <button 
        onClick={async () => {
          const res = await axios.get(`/api/v1/meetings/${selectedMeeting.id}/export/pdf`, { responseType: 'blob' })
          const url = window.URL.createObjectURL(new Blob([res.data]))
          const element = document.createElement('a')
          element.setAttribute('href', url)
          element.setAttribute('download', `${selectedMeeting.title}.pdf`)
          element.style.display = 'none'
          document.body.appendChild(element)
          element.click()
          document.body.removeChild(element)
        }}
        style={{ padding: '10px 20px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
      >
        📄 Download PDF
      </button>
    </div>

    {selectedMeeting.summary && (
              <div style={{ 
  marginTop: '20px', 
  padding: '15px', 
  border: `1px solid ${darkMode ? '#333' : '#ddd'}`,
  borderRadius: '5px',
  backgroundColor: darkMode ? '#2a2a2a' : '#f9f9f9'
}}>
                <h2>Summary</h2>
                <p>{selectedMeeting.summary}</p>
              </div>
            )}

            {selectedMeeting.transcript && (
              <div style={{ 
  marginTop: '20px', 
  padding: '15px', 
  border: `1px solid ${darkMode ? '#333' : '#ddd'}`,
  borderRadius: '5px',
  backgroundColor: darkMode ? '#2a2a2a' : '#f9f9f9'
}}>
                <h2>Transcript</h2>
                <p style={{ whiteSpace: 'pre-wrap', fontSize: '12px' }}>{selectedMeeting.transcript}</p>
              </div>
            )}

            {selectedMeeting.action_items && (
              <div style={{ 
  marginTop: '20px', 
  padding: '15px', 
  border: `1px solid ${darkMode ? '#333' : '#ddd'}`,
  borderRadius: '5px',
  backgroundColor: darkMode ? '#2a2a2a' : '#f9f9f9'
}}>
                <h2>Action Items</h2>
                <pre>{selectedMeeting.action_items}</pre>
              </div>
            )}
          </>
        ) : (
          <p>Meeting is still processing... Check back in a moment.</p>
        )}
      </div>
    )
  }

  // List View
  return (
    <div style={{ 
  maxWidth: '800px', 
  margin: '0 auto', 
  padding: '20px', 
  fontFamily: 'Arial',
  backgroundColor: darkMode ? '#1a1a1a' : '#ffffff',
  color: darkMode ? '#ffffff' : '#000000',
  minHeight: '100vh',
  transition: 'all 0.3s ease'
}}>
  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
    <div>
      <h1>🎙️ MeetingMind</h1>
      <p>AI-powered meeting transcription with Groq + Ollama</p>
    </div>
    <button 
      onClick={() => setDarkMode(!darkMode)}
      style={{ padding: '10px 15px', fontSize: '20px', cursor: 'pointer', border: 'none', borderRadius: '5px', backgroundColor: darkMode ? '#333' : '#eee' }}
    >
      {darkMode ? '☀️' : '🌙'}
    </button>
  </div>
      <form onSubmit={handleUpload} style={{ marginBottom: '30px' }}>
        <div style={{ marginBottom: '10px' }}>
          <label>Meeting Title:</label><br />
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g., Team Standup"
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label>Audio File:</label><br />
          <input
  type="file"
  accept="audio/*"
  multiple
  onChange={(e) => {
    setFiles(Array.from(e.target.files || []))
  }}
            style={{ marginTop: '5px' }}
          />
        </div>

        <button type="submit" disabled={loading} style={{ padding: '10px 20px', cursor: 'pointer' }}>
          {loading ? `Uploading (${files.length} files)...` : `Upload ${files.length} Meeting${files.length !== 1 ? 's' : ''}`}
        </button>

        {status && <p style={{ marginTop: '10px', color: 'green' }}>{status}</p>}
      </form>

      <h2>Recent Meetings ({meetings.length})</h2>

<div style={{ marginBottom: '20px' }}>
  <input
    type="text"
    placeholder="🔍 Search meetings by title..."
    onChange={async (e) => {
      const query = e.target.value
      if (query.trim()) {
        try {
          const res = await axios.get(`/api/v1/meetings/search?query=${encodeURIComponent(query)}`)
          setMeetings(res.data)
        } catch (err) {
          console.error('Search error:', err)
        }
      } else {
        loadMeetings() // Reload all if search is cleared
      }
    }}
    style={{ 
      width: '100%', 
      padding: '10px', 
      fontSize: '14px',
      border: '1px solid #ddd',
      borderRadius: '5px',
      marginBottom: '10px'
    }}
  />
</div>
      {meetings.length === 0 ? (
        <p>No meetings yet. Upload one to get started!</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {meetings.map(m => (
            <li 
              key={m.id} 
              onClick={() => handleSelectMeeting(m)}
              style={{ 
                marginBottom: '10px', 
                padding: '15px', 
                border: '1px solid #ddd',
                borderRadius: '5px',
                cursor: 'pointer',
                backgroundColor: '#f9f9f9'
              }}
            >
              <strong>{m.title}</strong><br />
              Status: <span style={{ color: m.status === 'completed' ? 'green' : 'orange' }}>
                {m.status}
              </span><br />
              <small>{new Date(m.created_at).toLocaleDateString()}</small>
              
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}