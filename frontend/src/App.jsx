import { useEffect, useState } from 'react'

const API = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export default function App() {
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Welcome! This starter app is ready. Connect your team’s chosen AI provider in backend/.env.' }
  ])
  const [conversationId, setConversationId] = useState(null)
  const [status, setStatus] = useState('Checking backend…')
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    fetch(`${API}/health`)
      .then(r => { if (!r.ok) throw new Error(); return r.json() })
      .then(() => setStatus('Backend connected'))
      .catch(() => setStatus('Backend unavailable — start FastAPI on port 8000'))
  }, [])

  async function sendMessage(e) {
    e.preventDefault()
    const trimmed = message.trim()
    if (!trimmed || busy) return

    setMessages(prev => [...prev, { role: 'user', text: trimmed }])
    setMessage('')
    setBusy(true)

    try {
      const response = await fetch(`${API}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: trimmed, conversation_id: conversationId })
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Request failed')
      if (data.conversation_id) setConversationId(data.conversation_id)
      setMessages(prev => [...prev, { role: 'assistant', text: data.reply }])
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', text: `Error: ${error.message}` }])
    } finally {
      setBusy(false)
    }
  }

  return (
    <main className="shell">
      <header className="topbar">
        <div className="mark">CX</div>
        <div>
          <p className="eyebrow">CROSSPOINTX 2026</p>
          <h1>Build something useful.</h1>
        </div>
        <span className="status">{status}</span>
      </header>

      <section className="intro">
        <p className="eyebrow">YOUR TEAM PROJECT</p>
        <h2>Turn an idea into a working prototype.</h2>
        <p className="muted">Replace this starter content with your chosen track, user problem and core feature.</p>
      </section>

      <section className="chat-card">
        <div className="card-heading">
          <div><p className="eyebrow">AI PROTOTYPE</p><h3>Test your integration</h3></div>
          <span className="live-dot">● Demo</span>
        </div>
        <div className="messages" aria-live="polite">
          {messages.map((item, index) => (
            <div className={`bubble ${item.role}`} key={index}>
              <span className="role">{item.role === 'user' ? 'YOU' : 'ASSISTANT'}</span>
              <p>{item.text}</p>
            </div>
          ))}
          {busy && <div className="bubble assistant"><p>Thinking…</p></div>}
        </div>
        <form onSubmit={sendMessage} className="composer">
          <input
            value={message}
            onChange={e => setMessage(e.target.value)}
            placeholder="Type a test message…"
            aria-label="Message"
          />
          <button disabled={busy || !message.trim()}>{busy ? 'Sending…' : 'Send'}</button>
        </form>
        <p className="hint">Prototype scaffold — do not enter private or sensitive information.</p>
      </section>
      <footer>CrossPointX 2026 · Team prototype starter</footer>
    </main>
  )
}
