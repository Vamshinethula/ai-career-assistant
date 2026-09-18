import { useCallback, useState } from 'react'
import Dashboard from './components/Dashboard'
import LoginForm from './components/LoginForm'
import RegisterForm from './components/RegisterForm'
import './App.css'

function App() {
  const [accessToken, setAccessToken] = useState(null)
  const [sessionMessage, setSessionMessage] = useState('')
  const handleSessionExpired = useCallback((message) => {
    setAccessToken(null)
    setSessionMessage(message)
  }, [])

  function handleLogin(token) {
    setSessionMessage('')
    setAccessToken(token)
  }
  return (
    <main className="welcome">
      <a className="skip-link" href="#workspace">Skip to {accessToken ? 'dashboard' : 'account forms'}</a>
      <header className="welcome-header">
        <p className="eyebrow">Your next chapter starts here</p>
        <h1>AI Career Assistant</h1>
        <p className="introduction">
          Turn your experience into a clearer career direction.
        </p>
      </header>

      <section className="overview" aria-labelledby="overview-title">
        <h2 id="overview-title">Explore your resume</h2>
        <p className="availability">Upload a resume, review detected skills and compare example roles.</p>
        <ol className="feature-list">
          <li>
            <h3>Bring your experience</h3>
            <p>Upload a readable PDF, up to 5 MiB and 10 pages, and review its extracted text.</p>
          </li>
          <li>
            <h3>Understand your skills</h3>
            <p>Review skill mentions detected using our local keyword catalog.</p>
          </li>
          <li>
            <h3>Explore your next step</h3>
            <p>Compare detected skills with example role profiles. Overlap scores are not hiring predictions.</p>
          </li>
        </ol>
      </section>
      <div id="workspace" tabIndex={-1}>
      {import.meta.env.MODE === 'demo' && (
        <aside className="demo-notice" aria-labelledby="demo-title">
          <h2 id="demo-title">Disposable portfolio demo</h2>
          <p>Use fictional account details, a unique test password, and a synthetic resume. Do not upload personal information.</p>
          <p>Accounts and uploaded resumes may disappear when the demo sleeps, restarts, or is updated. If your account has reset, register again.</p>
          <p>The server may take about a minute to wake up. If a request fails, wait and try again.</p>
        </aside>
      )}
      {accessToken ? (
        <Dashboard accessToken={accessToken} onLogout={() => setAccessToken(null)}
          onSessionExpired={handleSessionExpired} />
      ) : (
        <>
          {sessionMessage && <p role="alert">{sessionMessage}</p>}
          <RegisterForm />
          <LoginForm onLogin={handleLogin} />
        </>
      )}
      </div>
    </main>
  )
}

export default App
