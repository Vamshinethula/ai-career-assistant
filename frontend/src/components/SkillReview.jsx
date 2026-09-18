import { useState } from 'react'

function SkillReview({ resumeId, match }) {
  const [reviewed, setReviewed] = useState([])
  const skills = match.not_detected_skills

  function toggleSkill(skill) {
    setReviewed((previous) => previous.includes(skill)
      ? previous.filter((item) => item !== skill)
      : [...previous, skill])
  }

  return (
    <details className="skill-review" id={`skill-review-${resumeId}-${match.role_id}`}>
      <summary>Review next steps for {match.title}</summary>
      {skills.length === 0 ? (
        <p>All terms in this example profile were detected. Review your resume for concrete,
          truthful examples of using them; keyword coverage does not establish proficiency.</p>
      ) : (
        <>
          <p>For each term below, check whether your resume already describes it using different
            wording. If you have used it, describe a truthful project example. If it is new to
            you and relevant to your goal, choose a small practice project before adding it.</p>
          <p>Checking a box means you reviewed the term, not that you learned or mastered the skill.</p>
          <p className="registration-note">Progress is temporary. Hiding role overlaps, switching
            resumes, refreshing, or logging out clears this checklist.</p>
          <p role="status">{reviewed.length} of {skills.length} terms reviewed for {match.title}.</p>
          <ul className="skill-review-list">
            {skills.map((skill) => (
              <li key={skill}>
                <label>
                  <input type="checkbox" checked={reviewed.includes(skill)}
                    onChange={() => toggleSkill(skill)} />
                  Reviewed {skill}
                </label>
              </li>
            ))}
          </ul>
        </>
      )}
    </details>
  )
}

export default SkillReview
