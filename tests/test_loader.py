import json
import pytest
from pathlib import Path
from quiz.loader import load_questions, filter_by_domain


# Test that a valid questions file loads without error.
def test_load_valid_questions(tmp_path):
    questions_file = tmp_path / "questions.json"
    questions_file.write_text(json.dumps([
        {
            "id": "GH-300-001",
            "domain": "D1",
            "question": "Test question?",
            "options": {"a": "Option A", "b": "Option B"},
            "answers": ["a"],
            "explanation": "This is a test."
        }
    ]))
    
    # Load should succeed without raising an error.
    result = load_questions(questions_file)
    assert len(result) == 1
    assert result[0]["id"] == "GH-300-001"


# Test that missing required fields raises ValueError.
def test_load_missing_field(tmp_path):
    questions_file = tmp_path / "questions.json"
    questions_file.write_text(json.dumps([
        {
            "id": "GH-300-001",
            "domain": "D1",
            # Missing "question" field
            "options": {"a": "Option A"},
            "answers": ["a"],
            "explanation": "Test."
        }
    ]))
    
    with pytest.raises(ValueError, match="missing fields"):
        load_questions(questions_file)


# Test that invalid domain raises ValueError.
def test_load_invalid_domain(tmp_path):
    questions_file = tmp_path / "questions.json"
    questions_file.write_text(json.dumps([
        {
            "id": "GH-300-001",
            "domain": "D4",  # Invalid domain
            "question": "Test?",
            "options": {"a": "Option A"},
            "answers": ["a"],
            "explanation": "Test."
        }
    ]))
    
    with pytest.raises(ValueError, match="invalid domain"):
        load_questions(questions_file)


# Test that duplicate IDs raise ValueError.
def test_load_duplicate_id(tmp_path):
    questions_file = tmp_path / "questions.json"
    questions_file.write_text(json.dumps([
        {
            "id": "GH-300-001",
            "domain": "D1",
            "question": "Test 1?",
            "options": {"a": "Option A"},
            "answers": ["a"],
            "explanation": "Test."
        },
        {
            "id": "GH-300-001",  # Duplicate
            "domain": "D1",
            "question": "Test 2?",
            "options": {"a": "Option A"},
            "answers": ["a"],
            "explanation": "Test."
        }
    ]))
    
    with pytest.raises(ValueError, match="duplicate id"):
        load_questions(questions_file)


# Test that empty answers list raises ValueError.
def test_load_empty_answers(tmp_path):
    questions_file = tmp_path / "questions.json"
    questions_file.write_text(json.dumps([
        {
            "id": "GH-300-001",
            "domain": "D1",
            "question": "Test?",
            "options": {"a": "Option A"},
            "answers": [],  # Empty
            "explanation": "Test."
        }
    ]))
    
    with pytest.raises(ValueError, match="answers must be a non-empty list"):
        load_questions(questions_file)


# Test that answer not in options raises ValueError.
def test_load_answer_not_in_options(tmp_path):
    questions_file = tmp_path / "questions.json"
    questions_file.write_text(json.dumps([
        {
            "id": "GH-300-001",
            "domain": "D1",
            "question": "Test?",
            "options": {"a": "Option A", "b": "Option B"},
            "answers": ["c"],  # Not in options
            "explanation": "Test."
        }
    ]))
    
    with pytest.raises(ValueError, match="answers .* are not in options"):
        load_questions(questions_file)


# Test filter_by_domain with specific domain.
def test_filter_by_domain_d1():
    questions = [
        {"id": "1", "domain": "D1", "question": "Q1?", "options": {"a": "A"}, "answers": ["a"], "explanation": "E1"},
        {"id": "2", "domain": "D2", "question": "Q2?", "options": {"a": "A"}, "answers": ["a"], "explanation": "E2"},
        {"id": "3", "domain": "D1", "question": "Q3?", "options": {"a": "A"}, "answers": ["a"], "explanation": "E3"},
    ]
    
    result = filter_by_domain(questions, "D1")
    assert len(result) == 2
    assert all(q["domain"] == "D1" for q in result)


# Test filter_by_domain with domain=None returns all.
def test_filter_by_domain_none():
    questions = [
        {"id": "1", "domain": "D1", "question": "Q1?", "options": {"a": "A"}, "answers": ["a"], "explanation": "E1"},
        {"id": "2", "domain": "D2", "question": "Q2?", "options": {"a": "A"}, "answers": ["a"], "explanation": "E2"},
        {"id": "3", "domain": "D3", "question": "Q3?", "options": {"a": "A"}, "answers": ["a"], "explanation": "E3"},
    ]
    
    result = filter_by_domain(questions, None)
    assert len(result) == 3


# Test filter_by_domain with domain that has no matches.
def test_filter_by_domain_no_matches():
    questions = [
        {"id": "1", "domain": "D1", "question": "Q1?", "options": {"a": "A"}, "answers": ["a"], "explanation": "E1"},
        {"id": "2", "domain": "D1", "question": "Q2?", "options": {"a": "A"}, "answers": ["a"], "explanation": "E2"},
    ]
    
    result = filter_by_domain(questions, "D3")
    assert len(result) == 0
