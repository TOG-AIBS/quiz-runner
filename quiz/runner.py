import random
from typing import Optional


# Run a complete quiz session, returning results for scoring.
def run_quiz(questions: list[dict]) -> tuple[list[dict], list[bool]]:
    """
    Conduct an interactive quiz.
    
    Returns:
      (all_questions_with_user_answers, correctness_list)
    """
    results = []
    correctness = []
    
    for q in questions:
        user_answer = ask_question(q)
        is_correct = validate_answer(user_answer, q["answers"])
        results.append({**q, "user_answer": user_answer})
        correctness.append(is_correct)
        show_result(is_correct, q)
    
    return results, correctness


# Display question and get user answer.
def ask_question(question: dict) -> list[str]:
    """
    Display a question with options and collect the user's answer.
    
    Returns:
      List of answer letters (e.g., ["a"] or ["a", "c"])
    """
    print(f"\n{question['question']}")
    for letter, text in question["options"].items():
        print(f"  {letter}) {text}")
    
    while True:
        user_input = input("\nYour answer (comma-separated for multiple): ").strip().lower()
        if not user_input:
            print("Please enter at least one answer.")
            continue
        
        # Parse answer: comma-separated, strip spaces
        answers = [a.strip() for a in user_input.split(",")]
        
        # Validate all answers are single letters and exist in options
        valid_options = question["options"].keys()
        if all(len(a) == 1 and a in valid_options for a in answers):
            return sorted(answers)  # Sort for consistent comparison
        
        print(f"Invalid answer. Please enter letters from {sorted(valid_options)}")


# Check if user answer matches correct answers (all-or-nothing).
def validate_answer(user_answer: list[str], correct_answers: list[str]) -> bool:
    """
    Validate user answer against correct answers.
    All-or-nothing: must match exactly.
    """
    return sorted(user_answer) == sorted(correct_answers)


# Display result and explanation.
def show_result(is_correct: bool, question: dict) -> None:
    """Show whether answer was correct and display explanation."""
    status = "[OK] Correct" if is_correct else "[FAIL] Incorrect"
    print(f"{status}")
    print(f"Explanation: {question['explanation']}")


# Calculate quiz score as percentage.
def calculate_score(correctness: list[bool]) -> float:
    """
    Calculate score as percentage.
    
    Returns:
      Percentage (0-100) rounded to 2 decimals.
    """
    if not correctness:
        return 0.0
    return round(100 * sum(correctness) / len(correctness), 2)


# Prompt user for optional name.
def prompt_for_username() -> Optional[str]:
    """Ask user for name, return None if they decline."""
    user_input = input("\nEnter your name to save in history (or press Enter to skip): ").strip()
    return user_input if user_input else None
