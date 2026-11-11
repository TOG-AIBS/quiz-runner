# Quiz Runner

A small command-line quiz app. It asks multiple-choice questions from `questions.json`, scores your answers, and saves results to `history.json`.

Python 3.14, standard library only (pytest for tests).

## Setup (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pytest
```

## Usage

```powershell
python -m quiz                # 5 random questions from all domains
python -m quiz --domain D1    # only one domain (D1, D2 or D3)
python -m quiz --count 10     # ask 10 questions
python -m quiz --history      # show past results
```

- Answer with a letter, e.g. `a`. For several answers use commas, e.g. `a,c`.
- Scoring is all-or-nothing per question.
- After the quiz you can enter your name to save the result, or press Enter to skip the name.

## Question format

```json
{
  "id": "GH-300-001",
  "domain": "D1",
  "question": "What is the purpose of git init?",
  "options": { "a": "...", "b": "..." },
  "answers": ["a"],
  "explanation": "Why this answer is correct."
}
```

Questions are validated on load: all fields required, `domain` must be D1-D3, ids unique, and each answer must be a key in `options`.

## Project layout

| Path | Purpose |
| --- | --- |
| `quiz/__main__.py` | Command-line entry point |
| `quiz/loader.py` | Loads and validates questions |
| `quiz/runner.py` | Asks questions, checks answers, scores |
| `quiz/history.py` | Saves and shows history |
| `tests/` | pytest tests |
| `questions.json` | Question bank |
| `history.json` | Saved results (auto-updated) |

## Tests

```powershell
python -m pytest
```
