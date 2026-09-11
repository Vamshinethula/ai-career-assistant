import { useState } from 'react'
import { loginUser } from '../services/api'
import './RegisterForm.css'

function LoginForm({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    if (isSubmitting) return
    setIsSubmitting(true)
    setMessage('')
    try {
      const result = await loginUser({ email: email.trim(), password })
      setPassword('')
      onLogin(result.access_token)
    } catch (error) {
      setMessage(error.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <section className="registration" aria-labelledby="login-title">
      <h2 id="login-title">Log in</h2>
      <p className="registration-note">Use the account you registered above.</p>
      <form className="registration-form" onSubmit={handleSubmit}
        onChange={() => setMessage('')}>
        <div className="form-field">
          <label htmlFor="login-email">Email (required)</label>
          <input id="login-email" name="email" type="email" autoComplete="username"
            value={email} onChange={(event) => setEmail(event.target.value)}
            disabled={isSubmitting} required />
        </div>
        <div className="form-field">
          <label htmlFor="login-password">Password (required)</label>
          <input id="login-password" name="password" type="password"
            autoComplete="current-password" value={password}
            onChange={(event) => setPassword(event.target.value)}
            disabled={isSubmitting} required />
        </div>
        <button className="form-submit" type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Logging in…' : 'Log in'}
        </button>
        <p className="form-message" role="status">{message}</p>
      </form>
    </section>
  )
}

export default LoginForm
