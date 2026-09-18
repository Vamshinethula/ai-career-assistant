import assert from 'node:assert/strict'
import test from 'node:test'
import { createComparisonExport } from '../src/services/comparisonExport.js'

const result = {
  resume_id: 7, method: 'keyword_overlap', text_available: true,
  skill_overlap_percent: 0, job_skills: ['Python'], matched_skills: [], not_detected_skills: ['Python'],
  requirements: [{ skill: 'Python', category: 'uncertain', evidence: [
    { text: 'Python "required"\n<script>synthetic</script>', category: 'uncertain' },
  ] }],
  access_token: 'must-not-export', resume_text: 'must-not-export',
}

test('preserves automatic/user provenance and literal evidence, excludes unrelated private fields', () => {
  const before = JSON.stringify(result)
  const text = createComparisonExport(result, { Python: 'required', Unknown: 'optional' }, new Date('2026-09-18T00:00:00Z'))
  const exported = JSON.parse(text)
  assert.equal(exported.requirements[0].automatic_category, 'uncertain')
  assert.equal(exported.requirements[0].user_choice, 'required')
  assert.equal(exported.requirements[0].evidence[0].text, result.requirements[0].evidence[0].text)
  assert.equal(exported.skill_overlap_percent, 0)
  assert.equal(exported.format, 'ai-career-assistant-comparison-v2')
  assert.equal(exported.reviewed_requirement_score.percent, 0)
  assert.deepEqual(exported.reviewed_requirement_score.confirmed_required_skills, ['Python'])
  assert.equal(exported.generated_at, '2026-09-18T00:00:00.000Z')
  assert(!text.includes('must-not-export'))
  assert(!text.includes('Unknown'))
  assert.equal(JSON.stringify(result), before)
})

test('no choice and reset are both exported as null', () => {
  for (const choices of [{}, { Python: '' }]) {
    assert.equal(JSON.parse(createComparisonExport(result, choices)).requirements[0].user_choice, null)
  }
})

test('unavailable comparison stays null rather than zero', () => {
  const exported = JSON.parse(createComparisonExport({ ...result, text_available: false,
    skill_overlap_percent: null, job_skills: [], not_detected_skills: [], requirements: [] }, {}))
  assert.equal(exported.skill_overlap_percent, null)
  assert.equal(exported.resume_text_available, false)
  assert.deepEqual(exported.requirements, [])
})
