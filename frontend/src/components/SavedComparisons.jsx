import { useEffect, useRef, useState } from 'react'
import { deleteSavedComparison, getSavedComparison, listSavedComparisons, renameSavedComparison } from '../services/api'
import { calculateReviewedScore } from '../services/reviewedScore'

const labels = { required: 'Required', optional: 'Optional / preferred', not_required: 'Explicitly not required', uncertain: 'Uncertain' }

function DeleteComparison({ saved, accessToken, onSessionExpired, onDeleted }) {
  const [confirming, setConfirming] = useState(false)
  const [pending, setPending] = useState(false)
  const [error, setError] = useState('')
  const request = useRef(null)
  useEffect(() => () => request.current?.abort(), [])
  async function remove() {
    if (request.current) return
    const controller = new AbortController()
    request.current = controller
    setPending(true); setError('')
    try {
      await deleteSavedComparison(saved.resume_id, saved.id, accessToken, controller.signal)
      if (!controller.signal.aborted) onDeleted()
    } catch (failure) {
      if (controller.signal.aborted) return
      if (failure.status === 401) onSessionExpired(failure.message)
      else setError(`${failure.message} Refresh the list if deletion may already have succeeded.`)
    } finally {
      request.current = null
      if (!controller.signal.aborted) setPending(false)
    }
  }
  return <div>
    {!confirming ? <button type="button" className="form-submit" onClick={() => setConfirming(true)}>Delete saved comparison</button>
      : <div>
        <p>Delete “{saved.title}” permanently? This removes only this saved snapshot. Your resume and PDF remain available.</p>
        <button type="button" className="form-submit" disabled={pending} onClick={remove}>{pending ? 'Deleting…' : 'Confirm delete'}</button>
        <button type="button" className="form-submit" disabled={pending} onClick={() => { setConfirming(false); setError('') }}>Cancel deletion</button>
      </div>}
    {error && <p role="alert">{error}</p>}
  </div>
}

function RenameComparison({ saved, accessToken, onSessionExpired, onRenamed }) {
  const [title, setTitle] = useState(saved.title)
  const [pending, setPending] = useState(false)
  const [error, setError] = useState('')
  const request = useRef(null)
  useEffect(() => () => request.current?.abort(), [])
  async function rename(event) {
    event.preventDefault()
    if (request.current) return
    const controller = new AbortController()
    request.current = controller
    setPending(true); setError('')
    try {
      await renameSavedComparison(saved.resume_id, saved.id, title.trim(), accessToken, controller.signal)
      if (!controller.signal.aborted) onRenamed()
    } catch (failure) {
      if (controller.signal.aborted) return
      if (failure.status === 401) onSessionExpired(failure.message)
      else setError(failure.message)
    } finally {
      request.current = null
      if (!controller.signal.aborted) setPending(false)
    }
  }
  return <form onSubmit={rename}>
    <label htmlFor={`rename-comparison-${saved.id}`}>Saved comparison title</label>
    <input id={`rename-comparison-${saved.id}`} value={title} maxLength={120} required disabled={pending}
      onChange={event => setTitle(event.target.value)} />
    <button type="submit" className="form-submit" disabled={pending || !title.trim()}>{pending ? 'Renaming…' : 'Rename comparison'}</button>
    {error && <p role="alert">{error}</p>}
  </form>
}

function SavedComparisons({ resumeId, accessToken, onSessionExpired, version }) {
  const [rows, setRows] = useState(null)
  const [selected, setSelected] = useState(null)
  const [saved, setSaved] = useState(null)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)
  const [offset, setOffset] = useState(0)
  const [searchInput, setSearchInput] = useState('')
  const [search, setSearch] = useState('')
  function changePage(nextOffset) {
    setOffset(nextOffset); setRows(null); setSelected(null); setSaved(null); setError('')
    setAttempt(value => value + 1)
  }
  useEffect(() => {
    const controller = new AbortController()
    async function load() {
      try {
        const listing = await listSavedComparisons(resumeId, accessToken, controller.signal, offset, search)
        if (!controller.signal.aborted) { setRows(listing); setError('') }
        if (selected !== null) {
          const detail = await getSavedComparison(resumeId, selected, accessToken, controller.signal)
          if (!controller.signal.aborted) setSaved(detail)
        }
      } catch (failure) {
        if (controller.signal.aborted) return
        if (failure.status === 401) onSessionExpired(failure.message)
        else setError(failure.message)
      }
    }
    load()
    return () => controller.abort()
  }, [resumeId, accessToken, onSessionExpired, version, selected, attempt, offset, search])
  const reviewed = saved ? calculateReviewedScore(saved.result, saved.label_choices) : null
  return <section aria-labelledby={`saved-title-${resumeId}`}>
    <h4 id={`saved-title-${resumeId}`}>Saved comparisons</h4>
    <form onSubmit={event => { event.preventDefault(); setSearch(searchInput.trim()); changePage(0) }}>
      <label htmlFor={`history-search-${resumeId}`}>Search saved titles</label>
      <input id={`history-search-${resumeId}`} type="search" maxLength={120} value={searchInput}
        onChange={event => setSearchInput(event.target.value)} />
      <button type="submit" className="form-submit">Search comparisons</button>
      <button type="button" className="form-submit" onClick={() => {
        setSearchInput(''); setSearch(''); changePage(0)
      }}>Clear search</button>
    </form>
    {search && <p>Showing titles containing: {search}</p>}
    <button type="button" className="form-submit" onClick={() => {
      changePage(0)
    }}>Refresh saved comparisons</button>
    {!rows && !error && <p role="status">Loading saved comparisons…</p>}
    {error && <p role="alert">{error} Use Refresh saved comparisons to retry.</p>}
    {rows?.length === 0 && <p>{offset === 0
      ? (search ? 'No saved comparisons match this title search.' : 'No saved comparisons for this resume.')
      : 'No saved comparisons on this page. Go back or refresh.'}</p>}
    <p>Page {offset / 10 + 1}</p>
    <button type="button" className="form-submit" disabled={!rows || offset === 0} onClick={() => changePage(offset - 10)}>Newer comparisons</button>
    <button type="button" className="form-submit" disabled={!rows || rows.length <= 10} onClick={() => changePage(offset + 10)}>Older comparisons</button>
    <ul>{rows?.slice(0, 10).map(row => <li key={row.id}>
      <button type="button" className="form-submit" onClick={() => {
        setSaved(null); setError(''); setSelected(row.id); setAttempt(value => value + 1)
      }}>Open saved comparison: {row.title}</button>
      <p>Saved {new Date(row.created_at).toLocaleString()}</p>
    </li>)}</ul>
    {selected !== null && !saved && !error && rows && <p role="status">Loading saved snapshot…</p>}
    {saved && <article>
      <h5>Saved snapshot: {saved.title}</h5>
      <RenameComparison key={`${saved.id}-${saved.title}`} saved={saved} accessToken={accessToken}
        onSessionExpired={onSessionExpired} onRenamed={() => changePage(0)} />
      <p>This is a read-only snapshot, not a recalculation. It survives login sessions while application storage is retained.
        Disposable demo resets can erase it.</p>
      <pre style={{ whiteSpace: 'pre-wrap', overflowWrap: 'anywhere' }}>{saved.job_description}</pre>
      <p>Saved keyword overlap: {saved.result.skill_overlap_percent === null ? 'Unavailable' : `${saved.result.skill_overlap_percent}%`}</p>
      <p>Saved reviewed overlap: {reviewed.percent === null ? 'Unavailable' : `${reviewed.percent}%`}</p>
      <p>{reviewed.detected_skills.length} of {reviewed.confirmed_required_skills.length} confirmed required terms detected;
        {' '}{reviewed.unreviewed_count} unreviewed; {reviewed.uncertain_count} uncertain.</p>
      <p>Detected in both: {saved.result.matched_skills.join(', ') || 'None.'}</p>
      <p>Not detected in resume: {saved.result.not_detected_skills.join(', ') || 'None.'}</p>
      <ul>{saved.result.requirements.map(row => <li key={row.skill}>
        <p>{row.skill} — Automatic: {labels[row.category]}; Your saved choice: {labels[saved.label_choices[row.skill]] || 'Use automatic label'}</p>
        <details className="skill-review"><summary>Saved source wording for {row.skill}</summary>
          {row.evidence.map((item, index) => <blockquote key={index}>{item.text}</blockquote>)}
        </details>
      </li>)}</ul>
      <p>Scores are keyword evidence, not proficiency or hiring suitability. Reviewed overlap covers only your confirmed subset.</p>
      <button type="button" className="form-submit" onClick={() => { setSelected(null); setSaved(null) }}>Close saved snapshot</button>
      <DeleteComparison key={saved.id} saved={saved} accessToken={accessToken} onSessionExpired={onSessionExpired}
        onDeleted={() => {
          changePage(0)
        }} />
    </article>}
  </section>
}

export default SavedComparisons
