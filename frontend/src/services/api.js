const API_BASE_URL = 'http://127.0.0.1:8000'

async function requestJson(path, options, messages) {
  let response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      signal: options.signal
        ? AbortSignal.any([options.signal, AbortSignal.timeout(15000)])
        : AbortSignal.timeout(15000),
    })
  } catch {
    throw new Error('Could not reach the server. Check that FastAPI is running and try again.')
  }

  if (!response.ok) {
    const error = new Error(messages[response.status] ?? messages.default)
    error.status = response.status
    throw error
  }

  try {
    return await response.json()
  } catch {
    throw new Error('The server returned an unexpected response. Please try again.')
  }
}

function postJson(path, details, messages) {
  return requestJson(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(details),
  }, messages)
}

export async function getCurrentUser(accessToken, signal) {
  const user = await requestJson('/users/me', {
    method: 'GET',
    headers: { Authorization: `Bearer ${accessToken}` },
    signal,
  }, {
    401: 'Your session is no longer valid. Please log in again.',
    default: 'Could not load your profile. Please try again.',
  })
  if (typeof user?.full_name !== 'string' || typeof user.email !== 'string') {
    throw new Error('The server returned an unexpected profile. Please try again.')
  }
  return user
}

export function registerUser(details) {
  return postJson('/auth/register', details, {
    409: 'This email is already registered. Use a different email.',
    422: 'Check your name, email, and password, then try again.',
    default: 'Account creation failed. Please try again later.',
  })
}

export async function uploadResume(file, accessToken, signal) {
  const body = new FormData()
  body.append('resume_file', file)
  const resume = await requestJson('/resumes/upload', {
    method: 'POST',
    headers: { Authorization: `Bearer ${accessToken}` },
    body,
    signal,
  }, {
    400: 'Choose a valid PDF resume and try again.',
    401: 'Your session is no longer valid. Please log in again.',
    422: 'Select a PDF file before uploading.',
    default: 'Upload could not be confirmed. The server may have saved the file. Please try again later.',
  })
  if (!Number.isInteger(resume?.id) || typeof resume.original_filename !== 'string') {
    throw new Error('The server returned an unexpected upload response. The file may have been saved.')
  }
  return resume
}

export async function getResumes(accessToken, signal) {
  const resumes = await requestJson('/resumes', {
    method: 'GET',
    headers: { Authorization: `Bearer ${accessToken}` },
    signal,
  }, {
    401: 'Your session is no longer valid. Please log in again.',
    default: 'Could not load your resumes. Please try again.',
  })
  if (!Array.isArray(resumes) || resumes.some((resume) =>
    !Number.isInteger(resume?.id) || typeof resume.original_filename !== 'string')) {
    throw new Error('The server returned an unexpected resume list. Please try again.')
  }
  return resumes
}

export async function getResume(resumeId, accessToken, signal) {
  const resume = await requestJson(`/resumes/${resumeId}`, {
    method: 'GET',
    headers: { Authorization: `Bearer ${accessToken}` },
    signal,
  }, {
    401: 'Your session is no longer valid. Please log in again.',
    404: 'This resume is no longer available.',
    default: 'Could not load the resume text. Please try again.',
  })
  if (resume?.id !== resumeId || typeof resume.original_filename !== 'string'
      || (resume.resume_text !== null && typeof resume.resume_text !== 'string')) {
    throw new Error('The server returned unexpected resume details. Please try again.')
  }
  return resume
}

export async function getResumeSkills(resumeId, accessToken, signal) {
  const result = await requestJson(`/resumes/${resumeId}/skills`, {
    method: 'GET',
    headers: { Authorization: `Bearer ${accessToken}` },
    signal,
  }, {
    401: 'Your session is no longer valid. Please log in again.',
    404: 'This resume is no longer available.',
    default: 'Could not load the resume skills. Please try again.',
  })
  if (result?.resume_id !== resumeId || result.method !== 'rule_based'
      || typeof result.text_available !== 'boolean' || !Array.isArray(result.skills)
      || result.skills.some((skill) => typeof skill !== 'string' || !skill.trim())
      || (!result.text_available && result.skills.length > 0)) {
    throw new Error('The server returned unexpected skill results. Please try again.')
  }
  return result
}

export async function loginUser(credentials) {
  const result = await postJson('/auth/login', credentials, {
    401: 'Invalid email or password.',
    422: 'Enter a valid email and password, then try again.',
    default: 'Login failed. Please try again later.',
  })
  if (typeof result?.access_token !== 'string' || !result.access_token.trim()
      || result.token_type !== 'bearer') {
    throw new Error('The server returned an unexpected login response. Please try again.')
  }
  return result
}
