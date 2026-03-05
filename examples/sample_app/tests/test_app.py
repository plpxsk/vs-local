"""Basic tests for the sample app."""

import sqlite3
import pytest

from examples.sample_app.app import (
    setup_database,
    create_user,
    create_task,
    get_user,
    get_user_tasks,
    format_user_report,
    format_task_report,
)


@pytest.fixture
def db():
    """Create an in-memory database for testing."""
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, role TEXT)"
    )
    c.execute(
        "CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT, description TEXT, "
        "user_id INTEGER, status TEXT, priority INTEGER)"
    )
    conn.commit()
    yield conn
    conn.close()


def test_create_user(db):
    uid = create_user(db, "Alice", "alice@example.com", "admin")
    assert uid == 1


def test_create_task(db):
    uid = create_user(db, "Alice", "alice@example.com", "admin")
    tid = create_task(db, "Fix bug", "Fix the login bug", uid, 1)
    assert tid == 1


def test_get_user_tasks(db):
    uid = create_user(db, "Alice", "alice@example.com", "admin")
    create_task(db, "Task 1", "Desc 1", uid, 1)
    create_task(db, "Task 2", "Desc 2", uid, 2)
    tasks = get_user_tasks(db, uid)
    assert len(tasks) == 2


def test_format_user_report(db):
    create_user(db, "Alice", "alice@example.com", "admin")
    report = format_user_report(db)
    assert "Alice" in report
    assert "Total: 1 users" in report


def test_format_task_report(db):
    uid = create_user(db, "Alice", "alice@example.com", "admin")
    create_task(db, "Fix bug", "Fix it", uid, 1)
    report = format_task_report(db)
    assert "Fix bug" in report
    assert "Total: 1 tasks" in report
