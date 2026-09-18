import { useEffect, useRef, useState } from 'react'
import { compareResumeToJob } from '../services/api'
import { createComparisonExport } from '../services/comparisonExport'

const categoryLabels = {
  required: 'Required', optional: 'Optional / preferred',
  not_required: 'Explicitly not required', uncertain: 'Uncertain — review wording',
}

function JobComparison({ resumeId, accessToken, onSessionExpired }) {
  const [description, setDescription] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [pending, setPending] = useState(false)
  const [labelChoices, setLabelChoices] = useState({})
  const [downloadError, setDownloadError] = useState('')
  const request = useRef(null)
  useEffect(() => () => request.current?.abort(), [])

  function downloadSummary() {
    setDownloadError('')
    let url
    const link = document.createElement('a')
    try {
      url = URL.createObjectURL(new Blob([createComparisonExport(result, labelChoices)],
        { type: 'application/json;charset=utf-8' }))
      link.href = url
      link.download = `resume-${resumeId}-comparison.json`
      document.body.appendChild(link)
      link.click()
    } catch {
      setDownloadError('Could not start the download. Please try again.')
    } finally {
      link.remove()
      if (url) window.setTimeout(() => URL.revokeObjectURL(url), 1000)
    }
  }

  async function submit(event) {
    event.preventDefault()
    if (pending) return
    setResult(null)
    setDownloadError('')
    setLabelChoices({})
    setError('')
    if (!description.trim() || description.length > 10000) {
      setError('Enter a job description between 1 and 10,000 characters, not just spaces.')
      return
    }
    const controller = new AbortController()
    request.current = controller
    setPending(true)
    try {
      const comparison = await compareResumeToJob(resumeId, description, accessToken, controller.signal)
      if (!controller.signal.aborted) setResult(comparison)
    } catch (failure) {
      if (controller.signal.aborted) return
      if (failure.status === 401) onSessionExpired(failure.message)
      else setError(failure.message)
    } finally {
      if (!controller.signal.aborted) setPending(false)
    }
  }

  return (
    <section id={`job-comparison-${resumeId}`} aria-labelledby={`job-title-${resumeId}`}>
      <h4 id={`job-title-${resumeId}`}>Compare with a job description</h4>
      <p>Paste text, not a link. It is sent to this app's backend for comparison,
        but is not saved or sent to an external AI service. Use synthetic text in the demo.</p>
      <form className="registration-form" onSubmit={submit}>
        <div className="form-field">
          <label htmlFor={`job-description-${resumeId}`}>Job description</label>
          <textarea id={`job-description-${resumeId}`} rows={7} required maxLength={10000}
            aria-describedby={`job-help-${resumeId}`} value={description} disabled={pending}
            onChange={(event) => {
              setDescription(event.target.value)
              setResult(null)
              setDownloadError('')
              setLabelChoices({})
              setError('')
            }} />
          <p id={`job-help-${resumeId}`}>{description.length.toLocaleString()} / 10,000 characters.
            Text and results clear when you close this comparison.</p>
        </div>
        <button className="form-submit" type="submit" disabled={pending}>
          {pending ? 'Comparing…' : 'Compare skills'}
        </button>
      </form>
      {pending && <p role="status">Comparing detected skill terms…</p>}
      {error && <p role="alert">{error} You can submit the comparison again.</p>}
      {result && <div aria-live="polite">
        <p>Download a JSON summary of these results and your label choices. It includes
          job-description source excerpts; review the file before sharing. It does not include
          your resume text or login token. The downloaded copy remains on your device after logout.</p>
        <button type="button" className="form-submit" onClick={downloadSummary}>Download comparison summary</button>
        {downloadError && <p role="alert">{downloadError}</p>}
        {!result.text_available
          ? <p>No readable resume text is available. Try a PDF with selectable text.</p>
          : result.job_skills.length === 0
            ? <p>No skills from our catalog were detected in this job description. There is not enough information to calculate overlap.</p>
            : <>
              <p><strong>{result.skill_overlap_percent}% job-description keyword overlap</strong></p>
              <p>{result.matched_skills.length} of {result.job_skills.length} detected job-description skills also appear in the resume.</p>
              <p>Every detected term counts equally, including optional or negated mentions.
                For example, “Python required; Docker optional” counts both Python and Docker.
                Review the original wording before using this score.</p>
              <p>Detected in job description: {result.job_skills.join(', ')}</p>
              <p>Detected in both: {result.matched_skills.join(', ') || 'None.'}</p>
              <p>Not detected in resume: {result.not_detected_skills.join(', ') || 'None among these terms.'}</p>
            </>}
        {result.requirements.length > 0 && <section aria-labelledby={`requirements-title-${resumeId}`}>
          <h5 id={`requirements-title-${resumeId}`}>Requirement wording to review</h5>
          <p>These tentative labels recognize a limited set of explicit phrases.
            Conflicting or unsupported wording stays uncertain. They do not change the keyword score.
            “Not required” does not mean a skill is prohibited.</p>
          <p>Your choices are temporary and do not change the score or automatic labels.
            Editing the text, comparing again, closing this panel, switching resumes,
            refreshing, or logging out clears them.</p>
          <ul className="requirement-results">
            {result.requirements.map((row, rowIndex) => <li key={row.skill}>
              <p><strong>{row.skill}: {categoryLabels[row.category]}</strong></p>
              <p>Automatic label: {categoryLabels[row.category]}</p>
              <details className="skill-review">
                <summary>Source wording for {row.skill}</summary>
                <ul>{row.evidence.map((item, index) => <li key={index}>
                  <blockquote>{item.text}</blockquote>
                  <p>Phrase label: {categoryLabels[item.category]}</p>
                </li>)}</ul>
              </details>
              <div className="form-field">
                <label htmlFor={`requirement-choice-${resumeId}-${rowIndex}`}>Your label for {row.skill}</label>
                <select id={`requirement-choice-${resumeId}-${rowIndex}`}
                  value={labelChoices[row.skill] || ''}
                  onChange={(event) => setLabelChoices((previous) => ({
                    ...previous, [row.skill]: event.target.value,
                  }))}>
                  <option value="">Use automatic label</option>
                  {Object.entries(categoryLabels).map(([value, label]) => (
                    <option key={value} value={value}>{label}</option>
                  ))}
                </select>
              </div>
              {labelChoices[row.skill] && <div>
                <p role="status">Your choice for {row.skill}: {categoryLabels[labelChoices[row.skill]]}</p>
                <button type="button" className="form-submit"
                  onClick={() => setLabelChoices((previous) => ({ ...previous, [row.skill]: '' }))}>
                  Reset label for {row.skill}
                </button>
              </div>}
            </li>)}
          </ul>
        </section>}
      </div>}
      <p className="registration-note">Keyword overlap is not a hiring prediction or proficiency score.
        The catalog may miss skills and context, including negation and required versus optional skills.
        A term not detected in your resume is not proof that you lack it.</p>
    </section>
  )
}

export default JobComparison
