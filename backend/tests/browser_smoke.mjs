// Run from project root with Node 24+: node backend/tests/browser_smoke.mjs
// Uses installed Chrome and Python environment; reserves ports 8001/9223.
import assert from 'node:assert/strict'
import { spawn } from 'node:child_process'
import { mkdtemp, readFile, rm } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import net from 'node:net'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..')
const demo = process.env.CAREER_TEST_DEMO === 'true'
const frontendPort = demo ? 5174 : 5173
const frontendUrl = `http://127.0.0.1:${frontendPort}`
const chrome = process.env.CAREER_TEST_CHROME || 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms))
for (const port of [8001, 9223, ...(demo ? [frontendPort] : [])]) {
  await new Promise((resolve, reject) => {
    const server = net.createServer()
    server.once('error', () => reject(new Error(`Port ${port} is in use; stop its dev server before this test.`)))
    server.listen(port, '127.0.0.1', () => server.close(resolve))
  })
}
const storage = await mkdtemp(path.join(tmpdir(), 'career-browser-test-'))
const children = []
let socket
let command
function start(executable, args, cwd) {
  const child = spawn(executable, args, {
    cwd, windowsHide: true, stdio: 'ignore',
    env: { ...process.env, CAREER_BROWSER_TEST_DIR: storage, PYTHONPATH: path.join(root, 'backend'),
      CORS_ORIGINS: frontendUrl, VITE_API_BASE_URL: 'http://127.0.0.1:8000' },
  })
  child.on('error', (error) => { child.startError = error })
  children.push(child)
}
async function until(check, label) {
  for (let i = 0; i < 100; i++) {
    if (children.some((child) => child.startError)) throw new Error('Could not start a test process; check installed paths.')
    if (await check()) return
    await wait(150)
  }
  throw new Error(`Timed out: ${label}`)
}
try {
  start(path.join(root, 'backend/.venv/Scripts/python.exe'), ['tests/browser_server.py'], path.join(root, 'backend'))
  let frontendRunning = false
  if (!demo) {
    try { frontendRunning = (await fetch(frontendUrl)).ok } catch { /* start below */ }
  }
  if (!frontendRunning) start(process.execPath, ['node_modules/vite/bin/vite.js', '--host', '127.0.0.1', '--port', String(frontendPort), '--strictPort', '--mode', demo ? 'demo' : 'development'], path.join(root, 'frontend'))
  for (const url of ['http://127.0.0.1:8001/health', frontendUrl]) {
    await until(async () => { try { return (await fetch(url)).ok } catch { return false } }, url)
  }
  start(chrome, ['--headless=new', '--no-first-run', '--no-default-browser-check',
    '--remote-debugging-port=9223', `--user-data-dir=${path.join(storage, 'profile')}`, 'about:blank'], root)
  let targets
  await until(async () => {
    try { targets = await (await fetch('http://127.0.0.1:9223/json')).json(); return targets.some((t) => t.type === 'page') }
    catch { return false }
  }, 'Chrome debugger')
  socket = new WebSocket(targets.find((t) => t.type === 'page').webSocketDebuggerUrl)
  await new Promise((resolve, reject) => { socket.onopen = resolve; socket.onerror = reject })
  let nextId = 0
  const pending = new Map()
  socket.onmessage = ({ data }) => {
    const message = JSON.parse(data)
    if (message.method === 'Fetch.requestPaused') {
      const { requestId, request } = message.params
      command('Fetch.continueRequest', { requestId,
        url: request.url.replace('http://127.0.0.1:8000/', 'http://127.0.0.1:8001/') }).catch(() => {})
      return
    }
    const handler = pending.get(message.id)
    if (handler) {
      pending.delete(message.id)
      clearTimeout(handler.timer)
      if (message.error) handler.reject(new Error(message.error.message))
      else handler.resolve(message.result)
    }
  }
  command = (method, params = {}) => new Promise((resolve, reject) => {
    const id = ++nextId
    const timer = setTimeout(() => { pending.delete(id); reject(new Error(`CDP timeout: ${method}`)) }, 10000)
    pending.set(id, { resolve, reject, timer })
    socket.send(JSON.stringify({ id, method, params }))
  })
  const evaluate = async (expression) => {
    const result = await command('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true })
    if (result.exceptionDetails) throw new Error('Browser evaluation failed')
    return result.result.value
  }
  const hasText = (text) => evaluate(`document.body.innerText.includes(${JSON.stringify(text)})`)
  const click = (text) => evaluate(`Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === ${JSON.stringify(text)}).click()`)
  const input = async (id, value) => {
    await evaluate(`document.getElementById(${JSON.stringify(id)}).focus()`)
    await command('Input.insertText', { text: value })
  }
  // Redirect this browser's API requests only; never submit test data to the real DB.
  await command('Fetch.enable', { patterns: [{ urlPattern: 'http://127.0.0.1:8000/*', requestStage: 'Request' }] })
  await command('Page.navigate', { url: frontendUrl })
  await until(() => hasText('Create your account'), 'registration form')
  assert.equal(await hasText('Disposable portfolio demo'), demo, 'Notice matches build mode')
  if (demo) assert(await hasText('Do not upload personal information.'))
  const pressKey = async (key, code, virtualKey) => {
    for (const type of ['keyDown', 'keyUp']) {
      await command('Input.dispatchKeyEvent', { type, key, code, windowsVirtualKeyCode: virtualKey })
    }
  }
  await pressKey('Tab', 'Tab', 9)
  assert(await evaluate("document.activeElement.matches('.skip-link')"), 'First Tab reaches skip link')
  assert(await evaluate("document.activeElement.getBoundingClientRect().top >= 0"), 'Focused skip link is visible')
  await pressKey('Enter', 'Enter', 13)
  assert(await evaluate("document.activeElement.id === 'workspace'"), 'Skip link focuses workspace')
  await pressKey('Tab', 'Tab', 9)
  assert(await evaluate("document.activeElement.id === 'full-name'"), 'Next Tab reaches registration input')
  assert(!(await hasText('These features are coming')), 'Overview describes implemented features')
  await input('full-name', 'Browser Test User')
  await input('email', 'browser@example.com')
  await input('password', 'a'.repeat(73))
  await evaluate("document.getElementById('full-name').form.requestSubmit()")
  await until(() => hasText('Use a password up to 72 bytes'), 'password length validation')
  await evaluate("document.getElementById('password').select()")
  await input('password', 'synthetic-test-password')
  await evaluate("document.getElementById('full-name').form.requestSubmit()")
  await until(() => hasText('Account created successfully'), 'registration success')
  await input('login-email', 'browser@example.com')
  await input('login-password', 'synthetic-test-password')
  await click('Log in')
  await until(() => hasText('Welcome, Browser Test User'), 'profile')
  assert.equal(await hasText('Disposable portfolio demo'), demo, 'Notice remains available after login')
  const { root: dom } = await command('DOM.getDocument')
  const { nodeId } = await command('DOM.querySelector', { nodeId: dom.nodeId, selector: '#resume-file' })
  for (const [filename, message] of [
    ['oversized.pdf', 'Choose a PDF no larger than 5 MiB.'],
    ['corrupt.pdf', 'Choose a nonempty, readable PDF without password protection.'],
    ['too-many-pages.pdf', 'Choose a PDF no larger than 5 MiB and no more than 10 pages.'],
  ]) {
    await command('DOM.setFileInputFiles', { nodeId, files: [path.join(storage, filename)] })
    await click('Upload resume')
    await until(() => hasText(message), `rejection of ${filename}`)
  }
  await command('DOM.setFileInputFiles', { nodeId, files: [path.join(storage, 'sample.pdf')] })
  await click('Upload resume')
  await until(() => hasText('Uploaded sample.pdf successfully.'), 'upload')
  await until(() => hasText('View text'), 'list refresh')
  await click('View text')
  await until(() => hasText('Python FastAPI SQL Git Docker'), 'extracted text')
  await click('View skills')
  await until(() => evaluate("document.querySelector('[id^=resume-skills-] ul')?.innerText.includes('FastAPI')"), 'skills')
  await click('View role overlaps')
  await until(() => hasText('100% skill overlap'), 'role overlap')
  assert(await hasText('5 of 5 profile skills detected.'))
  const reviewSelector = '[id$="-java_backend"].skill-review'
  await evaluate(`document.querySelector('${reviewSelector} summary').focus()`)
  assert(await evaluate(`document.activeElement === document.querySelector('${reviewSelector} summary')`), 'Review summary receives focus')
  await pressKey(' ', 'Space', 32)
  await until(() => evaluate(`document.querySelector('${reviewSelector}').open`), 'keyboard expands skill review')
  await until(() => hasText('0 of 2 terms reviewed for Java backend developer.'), 'review checklist')
  await evaluate(`document.querySelector('${reviewSelector} input').focus()`)
  await pressKey(' ', 'Space', 32)
  await until(() => hasText('1 of 2 terms reviewed for Java backend developer.'), 'review checkbox')
  assert(await hasText('60% skill overlap'), 'Review does not change the matching score')
  await pressKey(' ', 'Space', 32)
  await until(() => hasText('0 of 2 terms reviewed for Java backend developer.'), 'uncheck review')
  await pressKey(' ', 'Space', 32)
  await until(() => hasText('1 of 2 terms reviewed for Java backend developer.'), 'review before reset')
  await evaluate("document.querySelector('[id$=\"-python_backend\"].skill-review summary').click()")
  assert(await hasText('All terms in this example profile were detected.'))
  assert.equal(await evaluate("document.querySelectorAll('[id$=\"-python_backend\"].skill-review input').length"), 0)
  await click('Hide role overlaps')
  await command('Network.enable')
  await command('Network.setBlockedURLs', { urls: ['*://127.0.0.1:8000/resumes/*/matches'] })
  await click('View role overlaps')
  await until(() => hasText('Could not reach the server.'), 'network failure message')
  await command('Network.setBlockedURLs', { urls: [] })
  await click('Try again')
  await until(() => hasText('100% skill overlap'), 'retry recovery')
  await evaluate(`document.querySelector('${reviewSelector} summary').click()`)
  assert(await hasText('0 of 2 terms reviewed for Java backend developer.'), 'Reopened panel resets temporary progress')
  await click('Compare job description')
  const jobInputId = await evaluate("document.querySelector('textarea[id^=job-description-]').id")
  const replaceJobText = async (text) => {
    await evaluate(`document.getElementById(${JSON.stringify(jobInputId)}).select()`)
    await input(jobInputId, text)
  }
  await input(jobInputId, '   ')
  await click('Compare skills')
  await until(() => hasText('not just spaces.'), 'blank job description feedback')
  await replaceJobText('Python Docker Kubernetes')
  await click('Compare skills')
  await until(() => hasText('66.7% job-description keyword overlap'), 'job comparison')
  assert(await hasText('Not detected in resume: Kubernetes'))
  assert(await hasText('Every detected term counts equally, including optional or negated mentions.'))
  await replaceJobText('Team player with communication skills')
  assert(!(await hasText('66.7% job-description keyword overlap')), 'Editing clears stale comparison')
  await click('Compare skills')
  await until(() => hasText('There is not enough information to calculate overlap.'), 'uncatalogued job text')
  await replaceJobText('Python Docker Kubernetes')
  await command('Network.setBlockedURLs', { urls: ['*://127.0.0.1:8000/resumes/*/compare-job'] })
  await click('Compare skills')
  await until(() => hasText('You can submit the comparison again.'), 'job comparison network failure')
  await command('Network.setBlockedURLs', { urls: [] })
  await click('Compare skills')
  await until(() => hasText('66.7% job-description keyword overlap'), 'job comparison retry')
  await replaceJobText('Python is required. Docker is optional. Java is not required. SQL is required. SQL is optional.')
  await click('Compare skills')
  await until(() => hasText('75% job-description keyword overlap'), 'requirement comparison')
  for (const label of ['Python: Required', 'Docker: Optional / preferred', 'Java: Explicitly not required', 'SQL: Uncertain']) {
    assert(await hasText(label), `Requirement label ${label}`)
  }
  await evaluate("Array.from(document.querySelectorAll('summary')).find(s => s.textContent === 'Source wording for SQL').focus()")
  await pressKey(' ', 'Space', 32)
  await until(() => hasText('SQL is required.'), 'requirement evidence disclosure')
  assert(await hasText('SQL is optional.'))
  const sqlChoice = "Array.from(document.querySelectorAll('label')).find(l => l.textContent === 'Your label for SQL').control"
  await evaluate(`${sqlChoice}.focus()`)
  await pressKey('Home', 'Home', 36)
  await pressKey('ArrowDown', 'ArrowDown', 40)
  await pressKey('Tab', 'Tab', 9)
  await until(() => hasText('Your choice for SQL: Required'), 'keyboard label correction')
  assert(await hasText('100% reviewed requirement overlap'))
  assert(await hasText('1 of 1 user-confirmed required terms detected.'))
  assert(await hasText('3 terms not reviewed; 0 marked uncertain.'))
  assert(await hasText('SQL: Uncertain'), 'Automatic label remains visible')
  assert(await hasText('75% job-description keyword overlap'), 'Correction does not change score')
  await click('Reset label for SQL')
  assert(!(await hasText('Your choice for SQL:')), 'Reset removes user choice')
  assert(await hasText('No requirements confirmed yet.'))
  const chooseSql = () => evaluate(`(() => { const choice = ${sqlChoice}; choice.value = 'optional'; choice.dispatchEvent(new Event('change', {bubbles:true})); })()`)
  await chooseSql()
  await until(() => hasText('Your choice for SQL: Optional / preferred'), 'optional correction')
  await click('Compare skills')
  await until(() => hasText('75% job-description keyword overlap'), 'recompare resets correction')
  assert(!(await hasText('Your choice for SQL:')), 'Recompare removes user choices')
  await chooseSql()
  await until(() => hasText('Your choice for SQL:'), 'choice before editing')
  await replaceJobText('Python is required. Docker is optional. Java is not required. SQL is required. SQL is optional. ')
  assert(!(await hasText('Your choice for SQL:')), 'Editing clears corrections')
  await click('Compare skills')
  await until(() => hasText('75% job-description keyword overlap'), 'comparison after editing')
  await chooseSql()
  await until(() => hasText('Your choice for SQL:'), 'choice before closing')
  const titleId = await evaluate("document.querySelector('input[id^=comparison-title-]').id")
  await input(titleId, 'Synthetic saved role')
  await command('Network.setBlockedURLs', { urls: ['*://127.0.0.1:8000/resumes/*/comparisons'] })
  await click('Save comparison')
  await until(() => hasText('Could not reach the server.'), 'save failure feedback')
  await command('Network.setBlockedURLs', { urls: [] })
  await click('Save comparison')
  await until(() => hasText('Comparison saved.'), 'save snapshot')
  await until(() => hasText('Open saved comparison: Synthetic saved role'), 'saved list refresh')
  await command('Browser.setDownloadBehavior', { behavior: 'allow', downloadPath: storage })
  await evaluate("window.originalCreateObjectURL = URL.createObjectURL; URL.createObjectURL = () => { throw new Error('synthetic failure') }")
  await click('Download comparison summary')
  await until(() => hasText('Could not start the download.'), 'download failure feedback')
  await evaluate('URL.createObjectURL = window.originalCreateObjectURL; delete window.originalCreateObjectURL')
  await click('Download comparison summary')
  const comparisonResumeId = jobInputId.replace('job-description-', '')
  let exportedSummary
  await until(async () => {
    try { exportedSummary = JSON.parse(await readFile(path.join(storage, `resume-${comparisonResumeId}-comparison.json`), 'utf8')); return true }
    catch { return false }
  }, 'downloaded summary file')
  assert.equal(exportedSummary.skill_overlap_percent, 75)
  assert.equal(exportedSummary.reviewed_requirement_score.percent, null)
  const exportedSql = exportedSummary.requirements.find(row => row.skill === 'SQL')
  assert.equal(exportedSql.automatic_category, 'uncertain')
  assert.equal(exportedSql.user_choice, 'optional')
  assert.equal(exportedSql.evidence.length, 2)
  assert(!('access_token' in exportedSummary) && !('resume_text' in exportedSummary))
  await command('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 1, mobile: true })
  assert(await evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Mobile horizontal overflow')
  await click('Hide job comparison')
  await click('Compare job description')
  assert.equal(await evaluate("document.querySelector('textarea[id^=job-description-]').value"), '')
  assert(!(await hasText('66.7% job-description keyword overlap')), 'Closing clears comparison')
  assert(!(await hasText('Requirement wording to review')), 'Closing clears requirement evidence')
  assert(!(await hasText('Download comparison summary')), 'No export for stale results')
  assert(!(await hasText('Your choice for SQL:')), 'Closing clears corrections')
  await replaceJobText('Python <img src=x onerror="window.evidenceExecuted=true"> is required.')
  await click('Compare skills')
  await until(() => hasText('Python: Uncertain'), 'unsupported source wording')
  await evaluate("Array.from(document.querySelectorAll('summary')).find(s => s.textContent === 'Source wording for Python').click()")
  assert(await hasText('<img src=x'), 'Source markup is visible as literal text')
  assert(await evaluate("!window.evidenceExecuted && !document.querySelector('.requirement-results img')"), 'Source text never becomes HTML')
  await click('Log out')
  await until(() => hasText('Create your account'), 'logout')
  assert(!(await hasText('100% skill overlap')))
  await input('login-email', 'browser@example.com')
  await input('login-password', 'synthetic-test-password')
  await click('Log in')
  await until(() => hasText('View text'), 'resume list after relogin')
  await click('Compare job description')
  await until(() => hasText('Open saved comparison: Synthetic saved role'), 'persisted saved list')
  await click('Open saved comparison: Synthetic saved role')
  await until(() => hasText('Saved snapshot: Synthetic saved role'), 'reopened saved snapshot')
  assert(await hasText('Saved keyword overlap: 75%'))
  assert(await hasText('SQL — Automatic: Uncertain; Your saved choice: Optional / preferred'))
  assert(await hasText('Saved reviewed overlap: Unavailable'))
  await click('Delete saved comparison')
  await click('Cancel deletion')
  assert(await hasText('Saved snapshot: Synthetic saved role'))
  await click('Delete saved comparison')
  await command('Network.setBlockedURLs', { urls: ['*://127.0.0.1:8000/resumes/*/comparisons/*'] })
  await click('Confirm delete')
  await until(() => hasText('Could not reach the server'), 'delete network failure')
  await command('Network.setBlockedURLs', { urls: [] })
  await click('Confirm delete')
  await until(() => hasText('No saved comparisons for this resume.'), 'deleted saved snapshot')
  assert(!(await hasText('Saved snapshot: Synthetic saved role')))
  await click('Refresh saved comparisons')
  await until(() => hasText('No saved comparisons for this resume.'), 'deletion persists after refresh')
  assert(await evaluate(`(async () => {
    const base = 'http://127.0.0.1:8000';
    const login = await fetch(base + '/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: 'browser@example.com', password: 'synthetic-test-password' }) });
    const session = await login.json();
    const headers = { Authorization: 'Bearer ' + session.access_token, 'Content-Type': 'application/json' };
    const resumes = await (await fetch(base + '/resumes', { headers })).json();
    for (let index = 0; index < 11; index++) {
      const response = await fetch(base + '/resumes/' + resumes[0].id + '/comparisons', { method: 'POST', headers, body: JSON.stringify({ title: 'Pagination role ' + index, job_description: 'Python required' }) });
      if (response.status !== 201) return false;
    }
    return true;
  })()`), 'seed synthetic history pages')
  await click('Refresh saved comparisons')
  await until(() => hasText('Open saved comparison: Pagination role 10'), 'newest history page')
  assert(!(await hasText('Open saved comparison: Pagination role 0')))
  await click('Older comparisons')
  await until(() => hasText('Open saved comparison: Pagination role 0'), 'older history page')
  assert(await hasText('Page 2'))
  assert(await evaluate("[...document.querySelectorAll('button')].find(b => b.textContent === 'Older comparisons').disabled"))
  await click('Newer comparisons')
  await until(() => hasText('Open saved comparison: Pagination role 10'), 'return to newest history page')
  const searchId = await evaluate("document.querySelector('input[id^=history-search-]').id")
  await input(searchId, 'ROLE 10')
  await click('Search comparisons')
  await until(() => hasText('Showing titles containing: ROLE 10'), 'applied title filter')
  await until(() => evaluate("[...document.querySelectorAll('button')].filter(b => b.textContent.startsWith('Open saved comparison:')).length === 1"), 'one filtered title')
  assert(await hasText('Open saved comparison: Pagination role 10'))
  await click('Clear search')
  await input(searchId, 'no matching title')
  await click('Search comparisons')
  await until(() => hasText('No saved comparisons match this title search.'), 'no title matches')
  await click('Clear search')
  await until(() => hasText('Open saved comparison: Pagination role 10'), 'clear restores history')
  await click('Open saved comparison: Pagination role 10')
  await until(() => hasText('Saved snapshot: Pagination role 10'), 'open rename target')
  const renameId = await evaluate("document.querySelector('input[id^=rename-comparison-]').id")
  await input(renameId, ' renamed')
  await click('Rename comparison')
  await until(() => hasText('Open saved comparison: Pagination role 10 renamed'), 'renamed history title')
  await click('Open saved comparison: Pagination role 10 renamed')
  await until(() => hasText('Saved snapshot: Pagination role 10 renamed'), 'persisted rename')
  assert(await evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Saved comparison mobile overflow')
  await click('Log out')
  await until(() => hasText('Create your account'), 'final logout')
  console.log('PASS: real Chrome keyboard navigation, auth, uploads, text/skills/roles, skill review, job comparison/validation/empty results/retry/reset, mobile overflow, logout.')
} finally {
  if (command && socket?.readyState === WebSocket.OPEN) {
    try { await command('Browser.close') } catch { /* process cleanup below */ }
  }
  socket?.close()
  for (const child of children) {
    if (child.exitCode === null) child.kill()
  }
  await wait(1000)
  // Only remove the uniquely created test directory under the system temp root.
  assert(path.dirname(storage) === path.resolve(tmpdir()) && path.basename(storage).startsWith('career-browser-test-'))
  await rm(storage, { recursive: true, force: true, maxRetries: 5, retryDelay: 300 })
}
