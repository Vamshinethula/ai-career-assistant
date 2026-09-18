import { useEffect, useState } from 'react'
import { getResumes } from '../services/api'
import ResumeText from './ResumeText'
import ResumeSkills from './ResumeSkills'
import ResumeMatches from './ResumeMatches'
import JobComparison from './JobComparison'

function ResumeList({ accessToken, onSessionExpired }) {
  const [resumes, setResumes] = useState(null)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)
  const [selectedId, setSelectedId] = useState(null)
  const [skillsId, setSkillsId] = useState(null)
  const [matchesId, setMatchesId] = useState(null)
  const [comparisonId, setComparisonId] = useState(null)

  useEffect(() => {
    const controller = new AbortController()
    getResumes(accessToken, controller.signal)
      .then((result) => {
        if (!controller.signal.aborted) setResumes(result)
      })
      .catch((failure) => {
        if (controller.signal.aborted) return
        if (failure.status === 401) onSessionExpired(failure.message)
        else setError(failure.message)
      })
    return () => controller.abort()
  }, [accessToken, onSessionExpired, attempt])

  function retry() {
    setError('')
    setResumes(null)
    setAttempt((previous) => previous + 1)
  }

  return (
    <section aria-labelledby="resume-list-title">
      <h3 id="resume-list-title">Your uploaded resumes</h3>
      {resumes === null && !error && <p role="status">Loading your resumes…</p>}
      {error && (
        <div>
          <p role="alert">{error}</p>
          <button className="form-submit" type="button" onClick={retry}>Try again</button>
        </div>
      )}
      {resumes?.length === 0 && <p>You have not uploaded a resume yet.</p>}
      {resumes?.length > 0 && (
        <ul>
          {resumes.map((resume) => (
            <li key={resume.id} style={{ overflowWrap: 'anywhere' }}>
              <p>{resume.original_filename}</p>
              <button type="button" className="form-submit"
                aria-expanded={selectedId === resume.id}
                aria-controls={selectedId === resume.id ? `resume-text-${resume.id}` : undefined}
                aria-label={`${selectedId === resume.id ? 'Hide' : 'View'} text for ${resume.original_filename}`}
                onClick={() => setSelectedId(selectedId === resume.id ? null : resume.id)}>
                {selectedId === resume.id ? 'Hide text' : 'View text'}
              </button>
              {selectedId === resume.id && <ResumeText resumeId={resume.id}
                accessToken={accessToken} onSessionExpired={onSessionExpired} />}
              <p>
                <button type="button" className="form-submit"
                  aria-expanded={skillsId === resume.id}
                  aria-controls={skillsId === resume.id ? `resume-skills-${resume.id}` : undefined}
                  aria-label={`${skillsId === resume.id ? 'Hide' : 'View'} skills for ${resume.original_filename}`}
                  onClick={() => setSkillsId(skillsId === resume.id ? null : resume.id)}>
                  {skillsId === resume.id ? 'Hide skills' : 'View skills'}
                </button>
              </p>
              {skillsId === resume.id && <ResumeSkills resumeId={resume.id}
                accessToken={accessToken} onSessionExpired={onSessionExpired} />}
              <p>
                <button type="button" className="form-submit"
                  aria-expanded={matchesId === resume.id}
                  aria-controls={matchesId === resume.id ? `resume-matches-${resume.id}` : undefined}
                  aria-label={`${matchesId === resume.id ? 'Hide' : 'View'} role overlaps for ${resume.original_filename}`}
                  onClick={() => setMatchesId(matchesId === resume.id ? null : resume.id)}>
                  {matchesId === resume.id ? 'Hide role overlaps' : 'View role overlaps'}
                </button>
              </p>
              {matchesId === resume.id && <ResumeMatches resumeId={resume.id}
                accessToken={accessToken} onSessionExpired={onSessionExpired} />}
              <p>
                <button type="button" className="form-submit"
                  aria-expanded={comparisonId === resume.id}
                  aria-controls={comparisonId === resume.id ? `job-comparison-${resume.id}` : undefined}
                  aria-label={`${comparisonId === resume.id ? 'Hide' : 'Compare'} job description for ${resume.original_filename}`}
                  onClick={() => setComparisonId(comparisonId === resume.id ? null : resume.id)}>
                  {comparisonId === resume.id ? 'Hide job comparison' : 'Compare job description'}
                </button>
              </p>
              {comparisonId === resume.id && <JobComparison key={resume.id} resumeId={resume.id}
                accessToken={accessToken} onSessionExpired={onSessionExpired} />}
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}

export default ResumeList
