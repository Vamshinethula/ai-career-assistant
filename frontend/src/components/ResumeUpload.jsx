import { useEffect, useRef, useState } from 'react'
import { uploadResume } from '../services/api'

function ResumeUpload({ accessToken, onSessionExpired, onUploaded }) {
  const [pending, setPending] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const request = useRef(null)

  useEffect(() => () => request.current?.abort(), [])

  async function handleSubmit(event) {
    event.preventDefault()
    if (pending) return
    const form = event.currentTarget
    const file = form.elements.resume_file.files[0]
    setError('')
    setMessage('')
    if (!file || !file.name.toLowerCase().endsWith('.pdf') || file.size === 0) {
      setError('Choose a nonempty PDF resume.')
      return
    }
    const controller = new AbortController()
    request.current = controller
    setPending(true)
    try {
      const resume = await uploadResume(file, accessToken, controller.signal)
      if (controller.signal.aborted) return
      setMessage(`Uploaded ${resume.original_filename} successfully.`)
      form.reset()
      onUploaded()
    } catch (failure) {
      if (controller.signal.aborted) return
      if (failure.status === 401) onSessionExpired(failure.message)
      else setError(failure.message)
    } finally {
      if (!controller.signal.aborted) setPending(false)
    }
  }

  return (
    <section aria-labelledby="upload-title">
      <h3 id="upload-title">Upload your resume</h3>
      <p>Choose a PDF with selectable text. Each upload saves a new resume.</p>
      <form className="registration-form" onSubmit={handleSubmit} aria-busy={pending}>
        <div className="form-field">
          <label htmlFor="resume-file">PDF resume</label>
          <input id="resume-file" name="resume_file" type="file" accept=".pdf,application/pdf"
            required disabled={pending} onChange={() => { setError(''); setMessage('') }} />
        </div>
        <button className="form-submit" type="submit" disabled={pending}>
          {pending ? 'Uploading…' : 'Upload resume'}
        </button>
        {error && <p role="alert">{error}</p>}
        <p role="status">{message}</p>
      </form>
    </section>
  )
}

export default ResumeUpload
