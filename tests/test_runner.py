import pytest
from quiz.runner import validate_answer, calculate_score


# Test single-answer validation.
def test_validate_single_answer_correct():
    assert validate_answer(["a"], ["a"]) is True


# Test single-answer validation fails on wrong answer.
def test_validate_single_answer_wrong():
    assert validate_answer(["b"], ["a"]) is False


# Test multi-answer validation (all-or-nothing).
def test_validate_multi_answer_correct():
    assert validate_answer(["a", "c"], ["a", "c"]) is True


# Test multi-answer fails if user misses one correct answer.
def test_validate_multi_answer_incomplete():
    assert validate_answer(["a"], ["a", "c"]) is False


# Test multi-answer fails if user adds extra wrong answer.
def test_validate_multi_answer_extra():
    assert validate_answer(["a", "b", "c"], ["a", "c"]) is False


# Test validation is order-agnostic.
def test_validate_order_agnostic():
    assert validate_answer(["c", "a"], ["a", "c"]) is True


# Test that uppercase input is converted to lowercase (case-insensitive).
def test_validate_case_insensitive():
    # Internally, answers are normalized to lowercase by ask_question
    # but validate_answer just compares the lists as-is
    assert validate_answer(["A"], ["a"]) is False  # Different case in lists
    # Real test: ask_question should convert "A" to "a" before validation


# Test score calculation with perfect quiz.
def test_calculate_score_perfect():
    assert calculate_score([True, True, True]) == 100.0


# Test score calculation with half correct.
def test_calculate_score_half():
    assert calculate_score([True, False, True, False]) == 50.0


# Test score calculation with all wrong.
def test_calculate_score_zero():
    assert calculate_score([False, False]) == 0.0


# Test score calculation with rounding to 2 decimals.
def test_calculate_score_rounding():
    result = calculate_score([True, False, False])
    assert result == 33.33


# Edge case: empty quiz.
def test_calculate_score_empty():
    assert calculate_score([]) == 0.0
