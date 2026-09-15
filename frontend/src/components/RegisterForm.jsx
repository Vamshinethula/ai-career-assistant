import { useState } from 'react'
import { registerUser } from '../services/api'
import './RegisterForm.css'

function RegisterForm() {
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    if (isSubmitting) return
    if (new TextEncoder().encode(password).length > 72 || password.includes('\0')) {
      setMessage('Use a password up to 72 bytes (some characters use more than one byte), without null characters.')
      return
    }
    setIsSubmitting(true)
    setMessage('')
    try {
      await registerUser({ full_name: fullName.trim(), email: email.trim(), password })
      setPassword('')
      setMessage('Account created successfully. You can now log in below.')
    } catch (error) {
      setMessage(error.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <section className="registration" aria-labelledby="registration-title">
      <h2 id="registration-title">Create your account</h2>
      <p id="registration-note" className="registration-note">
        Enter your details to create an account.
      </p>

      <form
        className="registration-form"
        onSubmit={handleSubmit}
        onChange={() => setMessage('')}
        aria-describedby="registration-note"
      >
        <div className="form-field">
          <label htmlFor="full-name">Full name (required)</label>
          <input
            id="full-name"
            disabled={isSubmitting}
            name="full_name"
            type="text"
            autoComplete="name"
            value={fullName}
            onChange={(event) => {
              setFullName(event.target.value)
              event.target.setCustomValidity('')
            }}
            onInvalid={(event) => {
              if (event.target.validity.patternMismatch) {
                event.target.setCustomValidity('Enter a name containing more than spaces.')
              }
            }}
            pattern=".*\S.*"
            required
          />
        </div>

        <div className="form-field">
          <label htmlFor="email">Email (required)</label>
          <input
            id="email"
            disabled={isSubmitting}
            name="email"
            type="email"
            autoComplete="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </div>

        <div className="form-field">
          <label htmlFor="password">Password (required)</label>
          <input
            id="password"
            disabled={isSubmitting}
            name="password"
            type="password"
            autoComplete="new-password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
        </div>

        <button className="form-submit" type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Creating account…' : 'Create account'}
        </button>
        <p className="form-message" role="status">{message}</p>
      </form>
    </section>
  )
}

export default RegisterForm
