import { useEffect, useState } from 'react'
import { getResume } from '../services/api'

function ResumeText({ resumeId, accessToken, onSessionExpired }) {
  const [resume, setResume] = useState(null)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    getResume(resumeId, accessToken, controller.signal)
      .then((result) => {
        if (!controller.signal.aborted) setResume(result)
      })
      .catch((failure) => {
        if (controller.signal.aborted) return
        if (failure.status === 401) onSessionExpired(failure.message)
        else setError(failure.message)
      })
    return () => controller.abort()
  }, [resumeId, accessToken, onSessionExpired, attempt])

  return (
    <div id={`resume-text-${resumeId}`}>
      {!resume && !error && <p role="status">Loading resume text…</p>}
      {error && <div>
        <p role="alert">{error}</p>
        <button type="button" className="form-submit" onClick={() => {
          setError('')
          setAttempt((previous) => previous + 1)
        }}>Try again</button>
      </div>}
      {resume && <>
        <h4>Extracted text</h4>
        {resume.resume_text?.trim()
          ? <pre style={{ whiteSpace: 'pre-wrap', overflowWrap: 'anywhere', fontFamily: 'inherit' }}>
            {resume.resume_text}
          </pre>
          : <p>No extracted text is available. Scanned PDFs may need text recognition.</p>}
      </>}
    </div>
  )
}

export default ResumeText
