import { useEffect, useState } from 'react'
import { getResumeSkills } from '../services/api'

function ResumeSkills({ resumeId, accessToken, onSessionExpired }) {
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    getResumeSkills(resumeId, accessToken, controller.signal)
      .then((skills) => {
        if (!controller.signal.aborted) setResult(skills)
      })
      .catch((failure) => {
        if (controller.signal.aborted) return
        if (failure.status === 401) onSessionExpired(failure.message)
        else setError(failure.message)
      })
    return () => controller.abort()
  }, [resumeId, accessToken, onSessionExpired, attempt])

  return (
    <div id={`resume-skills-${resumeId}`}>
      <h4>Skills mentioned in your resume</h4>
      {!result && !error && <p role="status">Loading skills…</p>}
      {error && <div>
        <p role="alert">{error}</p>
        <button type="button" className="form-submit" onClick={() => {
          setError('')
          setAttempt((previous) => previous + 1)
        }}>Try again</button>
      </div>}
      {result && <>
        {!result.text_available
          ? <p>No readable resume text is available. Try uploading a PDF with selectable text.</p>
          : result.skills.length === 0
            ? <p>No skills from our current software-development catalog matched this resume. This does not mean you have no skills.</p>
            : <ul>{result.skills.map((skill) => <li key={skill}>{skill}</li>)}</ul>}
        <p className="registration-note">
          These are keyword matches from a limited catalog. They may miss skills or include
          terms mentioned without experience; they do not measure proficiency.
        </p>
      </>}
    </div>
  )
}

export default ResumeSkills
