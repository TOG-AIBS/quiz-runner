import json
from pathlib import Path
from datetime import datetime
from typing import Optional


HISTORY_FILE = Path(__file__).resolve().parent.parent / "history.json"


# Save a quiz session to history.
def save_session(domain: Optional[str], count: int, score: float, user: Optional[str]) -> None:
    """Save quiz results to history.json."""
    session = {
        "domain": domain or "All",
        "count": count,
        "score": score,
        "timestamp": datetime.now().isoformat(),
    }
    if user:
        session["user"] = user
    
    # Load existing history or start fresh
    history = load_history()
    history.append(session)
    
    # Write back to file
    HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")


# Load all sessions from history file.
def load_history() -> list[dict]:
    """Load history from file, return empty list if file doesn't exist."""
    if not HISTORY_FILE.exists():
        return []
    return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))


# Get overall statistics.
def get_summary() -> dict:
    """
    Calculate summary stats: total quizzes and average score.
    
    Returns:
      {"total": int, "average_score": float}
    """
    history = load_history()
    if not history:
        return {"total": 0, "average_score": 0.0}
    
    scores = [s["score"] for s in history]
    avg = round(sum(scores) / len(scores), 2)
    return {"total": len(history), "average_score": avg}


# Get statistics per domain.
def get_domain_stats() -> dict:
    """
    Calculate stats for each domain (D1, D2, D3, All).
    
    Returns:
      {"D1": {"count": int, "avg_score": float}, ...}
    """
    history = load_history()
    stats = {}
    
    for domain in ["D1", "D2", "D3", "All"]:
        sessions = [s for s in history if s["domain"] == domain]
        if sessions:
            scores = [s["score"] for s in sessions]
            stats[domain] = {
                "count": len(sessions),
                "average_score": round(sum(scores) / len(scores), 2)
            }
    
    return stats


# Get the most recent N sessions.
def get_recent(n: int = 5) -> list[dict]:
    """Return the last N quiz sessions."""
    history = load_history()
    return history[-n:] if history else []


# Display formatted history.
def display_history() -> None:
    """Print summary, domain breakdown, and recent quizzes."""
    history = load_history()
    
    if not history:
        print("No quiz history yet. Take a quiz to get started!")
        return
    
    print("\n" + "="*60)
    print("QUIZ HISTORY")
    print("="*60)
    
    # Summary stats
    summary = get_summary()
    print(f"\nSUMMARY")
    print(f"  Total quizzes: {summary['total']}")
    print(f"  Average score: {summary['average_score']}%")
    
    # Domain breakdown
    print(f"\nBY DOMAIN")
    domain_stats = get_domain_stats()
    for domain in ["D1", "D2", "D3", "All"]:
        if domain in domain_stats:
            stats = domain_stats[domain]
            print(f"  {domain}: {stats['count']} quizzes, avg {stats['average_score']}%")
    
    # Recent quizzes
    recent = get_recent(5)
    print(f"\nRECENT QUIZZES")
    for session in recent:
        timestamp = session["timestamp"][:10]  # YYYY-MM-DD only
        domain = session["domain"]
        score = session["score"]
        user_info = f" ({session['user']})" if "user" in session else ""
        print(f"  {timestamp} | {domain} | {score}%{user_info}")
    
    print("="*60 + "\n")
