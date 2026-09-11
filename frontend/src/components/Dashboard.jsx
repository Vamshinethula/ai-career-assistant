import { useEffect, useState } from 'react'
import { getCurrentUser } from '../services/api'
import './RegisterForm.css'
import ResumeUpload from './ResumeUpload'
import ResumeList from './ResumeList'

function Dashboard({ accessToken, onLogout, onSessionExpired }) {
  const [user, setUser] = useState(null)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)
  const [resumeVersion, setResumeVersion] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    getCurrentUser(accessToken, controller.signal)
      .then((profile) => {
        if (!controller.signal.aborted) setUser(profile)
      })
      .catch((failure) => {
        // Ignore results from a dashboard that has been left or replaced.
        if (controller.signal.aborted) return
        if (failure.status === 401) {
          onSessionExpired(failure.message)
        } else {
          setError(failure.message)
        }
      })
    return () => controller.abort()
  }, [accessToken, attempt, onSessionExpired])

  function retry() {
    setError('')
    setUser(null)
    setAttempt((previous) => previous + 1)
  }

  return (
    <section className="registration" aria-labelledby="dashboard-title">
      <h2 id="dashboard-title">Your dashboard</h2>
      {!user && !error && <p role="status">Loading your profile…</p>}
      {error && (
        <div>
          <p role="alert">{error}</p>
          <button className="form-submit" type="button" onClick={retry}>Try again</button>
        </div>
      )}
      {user && (
        <div>
          <h3>Welcome, {user.full_name}</h3>
          <p>Email: {user.email}</p>
          <ResumeUpload accessToken={accessToken} onSessionExpired={onSessionExpired}
            onUploaded={() => setResumeVersion((previous) => previous + 1)} />
          <ResumeList key={resumeVersion} accessToken={accessToken} onSessionExpired={onSessionExpired} />
        </div>
      )}
      <p className="registration-note">Refreshing this page will sign you out.</p>
      <button className="form-submit" type="button" onClick={onLogout}>Log out</button>
    </section>
  )
}

export default Dashboard
