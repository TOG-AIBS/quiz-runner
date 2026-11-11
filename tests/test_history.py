import json
import pytest
from pathlib import Path
from quiz.history import save_session, load_history, get_summary, get_domain_stats, get_recent
import quiz.history as history_module


# Test saving a session to history.
def test_save_session(tmp_path, monkeypatch):
    # Redirect history file to tmp location
    test_history = tmp_path / "history.json"
    monkeypatch.setattr(history_module, "HISTORY_FILE", test_history)
    
    save_session("D1", 5, 85.5, "Alice")
    
    # Verify file was created and contains session
    assert test_history.exists()
    data = json.loads(test_history.read_text())
    assert len(data) == 1
    assert data[0]["domain"] == "D1"
    assert data[0]["score"] == 85.5
    assert data[0]["user"] == "Alice"


# Test saving multiple sessions.
def test_save_multiple_sessions(tmp_path, monkeypatch):
    test_history = tmp_path / "history.json"
    monkeypatch.setattr(history_module, "HISTORY_FILE", test_history)
    
    save_session("D1", 5, 90.0, "Alice")
    save_session("D2", 5, 70.0, "Bob")
    
    data = json.loads(test_history.read_text())
    assert len(data) == 2


# Test saving without username.
def test_save_session_no_user(tmp_path, monkeypatch):
    test_history = tmp_path / "history.json"
    monkeypatch.setattr(history_module, "HISTORY_FILE", test_history)
    
    save_session("D1", 5, 85.5, None)
    
    data = json.loads(test_history.read_text())
    assert "user" not in data[0]


# Test loading empty history (file doesn't exist).
def test_load_history_empty(tmp_path, monkeypatch):
    test_history = tmp_path / "history.json"
    monkeypatch.setattr(history_module, "HISTORY_FILE", test_history)
    
    result = load_history()
    assert result == []


# Test get_summary with no history.
def test_get_summary_empty(tmp_path, monkeypatch):
    test_history = tmp_path / "history.json"
    monkeypatch.setattr(history_module, "HISTORY_FILE", test_history)
    
    result = get_summary()
    assert result == {"total": 0, "average_score": 0.0}


# Test get_summary with sessions.
def test_get_summary_with_data(tmp_path, monkeypatch):
    test_history = tmp_path / "history.json"
    monkeypatch.setattr(history_module, "HISTORY_FILE", test_history)
    
    save_session("D1", 5, 100.0, "Alice")
    save_session("D1", 5, 80.0, "Bob")
    
    result = get_summary()
    assert result["total"] == 2
    assert result["average_score"] == 90.0


# Test get_domain_stats.
def test_get_domain_stats(tmp_path, monkeypatch):
    test_history = tmp_path / "history.json"
    monkeypatch.setattr(history_module, "HISTORY_FILE", test_history)
    
    save_session("D1", 5, 100.0, "Alice")
    save_session("D1", 5, 80.0, "Bob")
    save_session("D2", 5, 70.0, "Charlie")
    
    result = get_domain_stats()
    assert result["D1"]["count"] == 2
    assert result["D1"]["average_score"] == 90.0
    assert result["D2"]["count"] == 1
    assert result["D2"]["average_score"] == 70.0
    assert "D3" not in result  # No D3 sessions


# Test get_recent returns last N sessions.
def test_get_recent(tmp_path, monkeypatch):
    test_history = tmp_path / "history.json"
    monkeypatch.setattr(history_module, "HISTORY_FILE", test_history)
    
    for i in range(7):
        save_session("D1", 5, float(50 + i*5), None)
    
    recent = get_recent(3)
    assert len(recent) == 3
    # Should be the last 3 (scores 70, 75, 80)
    assert recent[0]["score"] == 70.0
    assert recent[2]["score"] == 80.0


# Test get_recent with fewer sessions than requested.
def test_get_recent_small_history(tmp_path, monkeypatch):
    test_history = tmp_path / "history.json"
    monkeypatch.setattr(history_module, "HISTORY_FILE", test_history)
    
    save_session("D1", 5, 85.0, None)
    
    recent = get_recent(5)
    assert len(recent) == 1
