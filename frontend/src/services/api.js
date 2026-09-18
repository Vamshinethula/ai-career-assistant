const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL?.trim() || 'http://127.0.0.1:8000').replace(/\/+$/, '')

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
    400: 'Choose a nonempty, readable PDF without password protection.',
    413: 'Choose a PDF no larger than 5 MiB and no more than 10 pages.',
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

export async function getResumeMatches(resumeId, accessToken, signal) {
  const result = await requestJson(`/resumes/${resumeId}/matches`, {
    method: 'GET',
    headers: { Authorization: `Bearer ${accessToken}` },
    signal,
  }, {
    401: 'Your session is no longer valid. Please log in again.',
    404: 'This resume is no longer available.',
    default: 'Could not load role overlaps. Please try again.',
  })
  const isSkillList = (value) => Array.isArray(value)
    && value.every((skill) => typeof skill === 'string' && skill.trim())
  if (result?.resume_id !== resumeId || result.method !== 'skill_overlap'
      || result.catalog !== 'illustrative_v1' || typeof result.text_available !== 'boolean'
      || !isSkillList(result.extracted_skills) || !Array.isArray(result.matches)
      || result.matches.some((match) => typeof match?.role_id !== 'string'
        || typeof match.title !== 'string' || !Number.isFinite(match.skill_overlap_percent)
        || match.skill_overlap_percent < 0 || match.skill_overlap_percent > 100
        || !isSkillList(match.matched_skills) || !isSkillList(match.not_detected_skills))
      || (!result.text_available && (result.extracted_skills.length || result.matches.length))) {
    throw new Error('The server returned unexpected role results. Please try again.')
  }
  return result
}

export async function compareResumeToJob(resumeId, jobDescription, accessToken, signal) {
  const result = await requestJson(`/resumes/${resumeId}/compare-job`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${accessToken}` },
    body: JSON.stringify({ job_description: jobDescription }),
    signal,
  }, {
    401: 'Your session is no longer valid. Please log in again.',
    404: 'This resume is no longer available.',
    422: 'Enter a job description between 1 and 10,000 characters, not just spaces.',
    default: 'Could not compare the job description. Please try again.',
  })
  const isSkills = (value) => Array.isArray(value)
    && value.every((skill) => typeof skill === 'string' && skill.trim())
    && new Set(value).size === value.length
  if (result?.resume_id !== resumeId || result.method !== 'keyword_overlap'
      || typeof result.text_available !== 'boolean'
      || !isSkills(result.job_skills) || !isSkills(result.matched_skills)
      || !isSkills(result.not_detected_skills)) {
    throw new Error('The server returned an unexpected comparison. Please try again.')
  }
  const combined = [...result.matched_skills, ...result.not_detected_skills]
  const expectedScore = result.text_available && result.job_skills.length
    ? 100 * result.matched_skills.length / result.job_skills.length : null
  // Allow one-decimal rounding; Python and JavaScript differ on exact ties.
  const validScore = expectedScore === null ? result.skill_overlap_percent === null
    : Number.isFinite(result.skill_overlap_percent) && result.skill_overlap_percent >= 0
      && result.skill_overlap_percent <= 100
      && Math.abs(result.skill_overlap_percent - expectedScore) <= 0.0500001
  if (new Set(combined).size !== combined.length || combined.length !== result.job_skills.length
      || combined.some((skill) => !result.job_skills.includes(skill))
      || (!result.text_available && result.matched_skills.length > 0)
      || !validScore) {
    throw new Error('The server returned an unexpected comparison. Please try again.')
  }
  const categories = ['required', 'optional', 'not_required', 'uncertain']
  if (!Array.isArray(result.requirements) || result.requirements.length !== result.job_skills.length
      || new Set(result.requirements.map((row) => row?.skill)).size !== result.requirements.length
      || result.requirements.some((row) => !result.job_skills.includes(row?.skill)
        || !categories.includes(row.category) || !Array.isArray(row.evidence) || !row.evidence.length
        || row.evidence.some((item) => typeof item?.text !== 'string' || !item.text.trim()
          || !jobDescription.includes(item.text) || !categories.includes(item.category))
        || row.category !== (new Set(row.evidence.map((item) => item.category)).size === 1
          ? row.evidence[0].category : 'uncertain'))) {
    throw new Error('The server returned unexpected requirement labels. Please try again.')
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
