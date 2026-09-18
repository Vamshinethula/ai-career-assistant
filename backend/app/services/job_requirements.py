"""Conservative explicit-phrase labels; no score changes or semantic guarantees."""
import re

from app.services.skill_extractor import SKILL_ALIASES, extract_skills


# Full-fragment matches prevent one cue leaking onto another clause's skills.
PATTERNS = (
    ('not_required', r'no experience with (.+?) is required'),
    ('not_required', r'(.+?) (?:is |are )?not required'),
    ('required', r'(.+?) (?:is |are )?not optional'),
    ('required', r'required(?: skills)?\s*:\s*(.+)'),
    ('optional', r'(?:optional|preferred)(?: skills)?\s*:\s*(.+)'),
    ('required', r'(.+?) (?:is |are )?required'),
    ('optional', r'(.+?) (?:is |are )?(?:optional|preferred)'),
)
ALIASES = sorted({alias for values in SKILL_ALIASES.values() for alias in values},
                 key=len, reverse=True)
ALIAS_PATTERN = re.compile(r'(?<![\w+#])(?:' + '|'.join(map(re.escape, ALIASES)) + r')(?![\w+#])')


def _explicit_list_category(fragment: str) -> str:
    normalized = ' '.join(fragment.casefold().split()).rstrip('.!?')
    for category, pattern in PATTERNS:
        match = re.fullmatch(pattern, normalized)
        if not match:
            continue
        skill_list = match.group(1)
        # Accept only known aliases joined by commas, ampersands or "and".
        # "or", unknown names and leftover prose require human interpretation.
        remainder = ALIAS_PATTERN.sub('', skill_list)
        remainder = re.sub(r'\band\b|[,\s&]', '', remainder)
        if not remainder and extract_skills(skill_list):
            return category
    return 'uncertain'


def classify_job_requirements(text: str) -> list[dict]:
    """Return one label per catalog skill and the source fragments behind it.

    No heading inheritance; conflicting or unclassified occurrences force
    uncertainty. Evidence is returned in memory, never saved by this service.
    """
    mentions: dict[str, list[dict]] = {}
    for raw_fragment in re.split(r'[;\n\r]+|(?<=[.!?])\s+', text):
        fragment = raw_fragment.strip()
        category = _explicit_list_category(fragment)
        for skill in extract_skills(fragment):
            evidence = {'text': fragment, 'category': category}
            if evidence not in mentions.setdefault(skill, []):
                mentions[skill].append(evidence)
    results = []
    for skill, evidence in sorted(mentions.items(), key=lambda item: item[0].casefold()):
        categories = {item['category'] for item in evidence}
        results.append({'skill': skill,
                        'category': next(iter(categories)) if len(categories) == 1 else 'uncertain',
                        'evidence': evidence})
    return results
