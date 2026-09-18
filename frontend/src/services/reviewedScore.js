export function calculateReviewedScore(result, labelChoices) {
  const confirmed = result.job_skills.filter((skill) => labelChoices[skill] === 'required')
  const detected = confirmed.filter((skill) => result.matched_skills.includes(skill))
  const choices = ['required', 'optional', 'not_required', 'uncertain']
  return {
    method: 'user_confirmed_required_keyword_overlap',
    confirmed_required_skills: confirmed,
    detected_skills: detected,
    not_detected_skills: confirmed.filter((skill) => !result.matched_skills.includes(skill)),
    unreviewed_count: result.job_skills.filter((skill) => !choices.includes(labelChoices[skill])).length,
    uncertain_count: result.job_skills.filter((skill) => labelChoices[skill] === 'uncertain').length,
    percent: result.text_available && confirmed.length
      ? Math.round(1000 * detected.length / confirmed.length) / 10 : null,
  }
}
