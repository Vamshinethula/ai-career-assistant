import { useEffect, useState } from 'react'
import { getResumeMatches } from '../services/api'
import SkillReview from './SkillReview'

function ResumeMatches({ resumeId, accessToken, onSessionExpired }) {
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    getResumeMatches(resumeId, accessToken, controller.signal)
      .then((matches) => {
        if (!controller.signal.aborted) setResult(matches)
      })
      .catch((failure) => {
        if (controller.signal.aborted) return
        if (failure.status === 401) onSessionExpired(failure.message)
        else setError(failure.message)
      })
    return () => controller.abort()
  }, [resumeId, accessToken, onSessionExpired, attempt])

  return (
    <div id={`resume-matches-${resumeId}`}>
      <h4>Example role overlaps</h4>
      <p>These simplified profiles are learning examples, not live vacancies.
        Percentages measure keyword overlap, not qualification or hiring chances.</p>
      {!result && !error && <p role="status">Loading role overlaps…</p>}
      {error && <div>
        <p role="alert">{error}</p>
        <button type="button" className="form-submit" onClick={() => {
          setError('')
          setAttempt((previous) => previous + 1)
        }}>Try again</button>
      </div>}
      {result && <>
        {!result.text_available
          ? <p>No readable resume text is available. Try a PDF with selectable text.</p>
          : result.extracted_skills.length === 0
            ? <p>No skills from our current catalog were detected, so there are no role overlaps to show.</p>
            : result.matches.length === 0
              ? <p>Detected skills do not overlap these example profiles. This does not rule out suitable roles.</p>
              : <ol>{result.matches.map((match) => (
                <li key={match.role_id}>
                  <h5>{match.title}</h5>
                  <p><strong>{match.skill_overlap_percent}% skill overlap</strong></p>
                  <p>{match.matched_skills.length} of {match.matched_skills.length + match.not_detected_skills.length} profile skills detected.</p>
                  <p>Matched: {match.matched_skills.join(', ')}</p>
                  <p>Not detected: {match.not_detected_skills.join(', ') || 'None in this example profile.'}</p>
                  <SkillReview resumeId={resumeId} match={match} />
                </li>
              ))}</ol>}
        <p className="registration-note">Not detected means absent from the matched terms,
          not necessarily a skill you lack. Keyword matching may miss context or skills.</p>
      </>}
    </div>
  )
}

export default ResumeMatches
