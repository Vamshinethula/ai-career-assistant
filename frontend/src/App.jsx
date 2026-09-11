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
      <header className="welcome-header">
        <p className="eyebrow">Your next chapter starts here</p>
        <h1>AI Career Assistant</h1>
        <p className="introduction">
          Turn your experience into a clearer career direction.
        </p>
      </header>

      <section className="overview" aria-labelledby="overview-title">
        <h2 id="overview-title">What you will be able to do</h2>
        <p className="availability">These features are coming as we build the app.</p>
        <ol className="feature-list">
          <li>
            <h3>Bring your experience</h3>
            <p>Upload a PDF resume to start building your career profile.</p>
          </li>
          <li>
            <h3>Understand your skills</h3>
            <p>Identify your strengths and areas you want to develop.</p>
          </li>
          <li>
            <h3>Explore your next step</h3>
            <p>Discover suitable roles and personalized career recommendations.</p>
          </li>
        </ol>
      </section>
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
    </main>
  )
}

export default App
