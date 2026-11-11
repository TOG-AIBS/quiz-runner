"""CLI entry point for quiz runner."""
import argparse
import random
from quiz.loader import load_questions, filter_by_domain
from quiz.runner import run_quiz, calculate_score, prompt_for_username
from quiz.history import save_session, display_history


def main():
    parser = argparse.ArgumentParser(
        description="Quiz runner: test your knowledge from questions.json"
    )
    parser.add_argument(
        "--domain",
        choices=["D1", "D2", "D3"],
        default=None,
        help="Quiz domain (D1, D2, D3, or None for all)"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="Number of questions to ask (default: 5)"
    )
    parser.add_argument(
        "--history",
        action="store_true",
        help="Show quiz history and progress"
    )
    
    args = parser.parse_args()
    
    # Show history and exit
    if args.history:
        display_history()
        return
    
    # Run quiz
    all_questions = load_questions()
    questions = filter_by_domain(all_questions, args.domain)
    
    if not questions:
        print(f"No questions found for domain {args.domain}")
        return
    
    # Shuffle and limit to requested count
    questions = random.sample(questions, min(args.count, len(questions)))
    
    print(f"\nStarting quiz: {len(questions)} questions")
    if args.domain:
        print(f"Domain: {args.domain}")
    print("="*50)
    
    # Run the quiz
    results, correctness = run_quiz(questions)
    score = calculate_score(correctness)
    
    # Show final score
    print("\n" + "="*50)
    print(f"FINAL SCORE: {score}% ({sum(correctness)}/{len(correctness)})")
    print("="*50)
    
    # Ask for name and save to history
    user = prompt_for_username()
    save_session(args.domain, len(questions), score, user)
    print("[OK] Quiz saved to history\n")


if __name__ == "__main__":
    main()
