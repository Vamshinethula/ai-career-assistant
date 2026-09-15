// Run from project root with Node 24+: node backend/tests/browser_smoke.mjs
// Uses installed Chrome and Python environment; reserves ports 8001/9223.
import assert from 'node:assert/strict'
import { spawn } from 'node:child_process'
import { mkdtemp, rm } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import net from 'node:net'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..')
const chrome = process.env.CAREER_TEST_CHROME || 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms))
for (const port of [8001, 9223]) {
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
    env: { ...process.env, CAREER_BROWSER_TEST_DIR: storage, PYTHONPATH: path.join(root, 'backend') },
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
  try { frontendRunning = (await fetch('http://127.0.0.1:5173/')).ok } catch { /* start below */ }
  if (!frontendRunning) start(process.execPath, ['node_modules/vite/bin/vite.js', '--host', '127.0.0.1', '--port', '5173', '--strictPort'], path.join(root, 'frontend'))
  for (const url of ['http://127.0.0.1:8001/health', 'http://127.0.0.1:5173/']) {
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
  await command('Page.navigate', { url: 'http://127.0.0.1:5173/' })
  await until(() => hasText('Create your account'), 'registration form')
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
  const { root: dom } = await command('DOM.getDocument')
  const { nodeId } = await command('DOM.querySelector', { nodeId: dom.nodeId, selector: '#resume-file' })
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
  await click('Hide role overlaps')
  await command('Network.enable')
  await command('Network.setBlockedURLs', { urls: ['*://127.0.0.1:8000/resumes/*/matches'] })
  await click('View role overlaps')
  await until(() => hasText('Could not reach the server.'), 'network failure message')
  await command('Network.setBlockedURLs', { urls: [] })
  await click('Try again')
  await until(() => hasText('100% skill overlap'), 'retry recovery')
  await command('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 1, mobile: true })
  assert(await evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Mobile horizontal overflow')
  await click('Log out')
  await until(() => hasText('Create your account'), 'logout')
  assert(!(await hasText('100% skill overlap')))
  console.log('PASS: real Chrome password validation, registration, login/CORS, upload, list, text, skills, roles, network failure/retry, mobile overflow, logout.')
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
