import { calculateReviewedScore } from './reviewedScore.js'

export function createComparisonExport(result, labelChoices, generatedAt = new Date()) {
  return JSON.stringify({
    format: 'ai-career-assistant-comparison-v2',
    generated_at: generatedAt.toISOString(),
    resume_id: result.resume_id,
    method: result.method,
    resume_text_available: result.text_available,
    skill_overlap_percent: result.skill_overlap_percent,
    reviewed_requirement_score: calculateReviewedScore(result, labelChoices),
    job_skills: result.job_skills,
    matched_skills: result.matched_skills,
    not_detected_skills: result.not_detected_skills,
    requirements: result.requirements.map((row) => ({
      skill: row.skill,
      automatic_category: row.category,
      user_choice: labelChoices[row.skill] || null,
      evidence: row.evidence.map((item) => ({ text: item.text, automatic_category: item.category })),
    })),
    notes: [
      'Keyword overlap counts all detected job terms equally; it is not a hiring prediction or proficiency score.',
      'Requirement labels are tentative. not_required means explicitly not required, not prohibited.',
      'User choices do not change the original keyword score. The separate reviewed score uses only user-confirmed Required terms.',
      'The reviewed score covers a selected subset, not all job requirements. Unreviewed and uncertain terms are excluded; 100% does not mean full job suitability.',
      'A null score means no readable resume text or no detected job-description skills.',
      'This file includes submitted source wording and may contain private information. Review before sharing.',
      'The export is generated in your browser. It is not saved by the app and cannot be imported back.',
    ],
  }, null, 2)
}
