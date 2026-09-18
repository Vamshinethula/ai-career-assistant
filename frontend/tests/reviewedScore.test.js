import assert from 'node:assert/strict'
import test from 'node:test'
import { calculateReviewedScore } from '../src/services/reviewedScore.js'

const result = { text_available: true, job_skills: ['Python', 'Docker', 'SQL'], matched_skills: ['Python', 'SQL'] }

test('no explicit confirmation produces null even when automatic skills match', () => {
  assert.equal(calculateReviewedScore(result, {}).percent, null)
  assert.equal(calculateReviewedScore(result, { Python: '', Docker: 'optional', SQL: 'uncertain' }).percent, null)
})
test('only confirmed required terms form the denominator and explain the score', () => {
  const score = calculateReviewedScore(result, { Python: 'required', Docker: 'required', SQL: 'optional', Unknown: 'required' })
  assert.equal(score.percent, 50)
  assert.deepEqual(score.confirmed_required_skills, ['Python', 'Docker'])
  assert.deepEqual(score.not_detected_skills, ['Docker'])
})
test('zero, full, fractional and unavailable results remain distinct', () => {
  assert.equal(calculateReviewedScore(result, { Docker: 'required' }).percent, 0)
  assert.equal(calculateReviewedScore(result, { Python: 'required' }).percent, 100)
  assert.equal(calculateReviewedScore(result, { Python: 'required', SQL: 'required', Docker: 'required' }).percent, 66.7)
  assert.equal(calculateReviewedScore({ ...result, text_available: false }, { Python: 'required' }).percent, null)
})
test('reports unreviewed and uncertain counts without modifying inputs', () => {
  const before = JSON.stringify(result)
  const score = calculateReviewedScore(result, { Python: 'required', Docker: 'uncertain' })
  assert.equal(score.unreviewed_count, 1)
  assert.equal(score.uncertain_count, 1)
  assert.equal(JSON.stringify(result), before)
})
