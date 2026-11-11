import json
from pathlib import Path

# Default to questions.json in the project root (one folder above quiz/),
# so it is found no matter which folder the program is started from.
DEFAULT_PATH = Path(__file__).resolve().parent.parent / "questions.json"
REQUIRED_FIELDS = ("id", "domain", "question", "options", "answers", "explanation")
VALID_DOMAINS = ("D1", "D2", "D3")


# Load questions from questions.json and validate that each has id, domain (D1-D3),
# question, options (dict of letters), answers (non-empty list of letters in options) and explanation.
def load_questions(path: str | Path = DEFAULT_PATH) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        questions = json.load(f)
    # Collect every problem first so the user can fix them all at once.
    problems = find_problems(questions)
    if problems:
        raise ValueError("Invalid questions file:\n" + "\n".join(problems))
    return questions


def find_problems(questions) -> list[str]:
    if not isinstance(questions, list):
        return ["The top level of the file must be a list of questions."]
    problems = []
    seen_ids = []  # a plain list works even when an id is not hashable
    for number, q in enumerate(questions, start=1):
        problems.extend(check_question(q, number))
        if isinstance(q, dict) and "id" in q:
            if q["id"] in seen_ids:
                problems.append(f"Question {number}: duplicate id {q['id']!r}.")
            seen_ids.append(q["id"])
    return problems


def check_question(q, number: int) -> list[str]:
    if not isinstance(q, dict):
        return [f"Question {number}: must be a JSON object."]
    missing = [field for field in REQUIRED_FIELDS if field not in q]
    if missing:
        return [f"Question {number}: missing fields {', '.join(missing)}."]
    problems = []
    if q["domain"] not in VALID_DOMAINS:
        problems.append(f"Question {number}: invalid domain {q['domain']!r}.")
    if not isinstance(q["options"], dict):
        problems.append(f"Question {number}: options must be a dict.")
    if not isinstance(q["answers"], list) or not q["answers"]:
        problems.append(f"Question {number}: answers must be a non-empty list.")
    elif isinstance(q["options"], dict):
        # Non-string answers can never be option keys, so they are reported as bad too.
        bad = [a for a in q["answers"] if not isinstance(a, str) or a not in q["options"]]
        if bad:
            problems.append(f"Question {number}: answers {bad} are not in options.")
    return problems


# Return questions from a specific domain, or all if domain is None.
def filter_by_domain(questions: list[dict], domain: str | None) -> list[dict]:
    if domain is None:
        return questions
    return [q for q in questions if q["domain"] == domain]