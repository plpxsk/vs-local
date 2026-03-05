"""Sample app - intentionally rough code for demo purposes.

This code has several issues for demonstrating code review and refactoring:
- Long functions
- Code duplication
- SQL injection vulnerability
- Poor error handling
- Magic numbers
"""

import sqlite3
import json


def setup_database():
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, role TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT, description TEXT, user_id INTEGER, status TEXT, priority INTEGER)")
    conn.commit()
    return conn


# SQL INJECTION VULNERABILITY - intentional for demo
def get_user(conn, username):
    c = conn.cursor()
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    c.execute(query)
    return c.fetchone()


def get_user_tasks(conn, user_id):
    c = conn.cursor()
    query = "SELECT * FROM tasks WHERE user_id = '" + str(user_id) + "'"
    c.execute(query)
    return c.fetchall()


def create_user(conn, name, email, role):
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email, role) VALUES (?, ?, ?)", (name, email, role))
    conn.commit()
    return c.lastrowid


def create_task(conn, title, description, user_id, priority):
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description, user_id, status, priority) VALUES (?, ?, ?, 'open', ?)", (title, description, user_id, priority))
    conn.commit()
    return c.lastrowid


# DUPLICATION - these two functions are nearly identical
def format_user_report(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    report = ""
    report = report + "=" * 50 + "\n"
    report = report + "USER REPORT\n"
    report = report + "=" * 50 + "\n"
    for user in users:
        report = report + f"ID: {user[0]}\n"
        report = report + f"Name: {user[1]}\n"
        report = report + f"Email: {user[2]}\n"
        report = report + f"Role: {user[3]}\n"
        report = report + "-" * 30 + "\n"
    report = report + f"Total: {len(users)} users\n"
    return report


def format_task_report(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    report = ""
    report = report + "=" * 50 + "\n"
    report = report + "TASK REPORT\n"
    report = report + "=" * 50 + "\n"
    for task in tasks:
        report = report + f"ID: {task[0]}\n"
        report = report + f"Title: {task[1]}\n"
        report = report + f"Description: {task[2]}\n"
        report = report + f"User ID: {task[3]}\n"
        report = report + f"Status: {task[4]}\n"
        report = report + f"Priority: {task[5]}\n"
        report = report + "-" * 30 + "\n"
    report = report + f"Total: {len(tasks)} tasks\n"
    return report


# LONG FUNCTION - does too many things
def process_bulk_import(conn, json_data):
    data = json.loads(json_data)
    results = {"users_created": 0, "tasks_created": 0, "errors": []}

    if "users" in data:
        for u in data["users"]:
            if "name" in u and "email" in u:
                if len(u["name"]) > 0 and len(u["email"]) > 0:
                    if "@" in u["email"]:
                        role = u.get("role", "user")
                        try:
                            uid = create_user(conn, u["name"], u["email"], role)
                            results["users_created"] += 1
                            if "tasks" in u:
                                for t in u["tasks"]:
                                    if "title" in t:
                                        priority = t.get("priority", 3)
                                        desc = t.get("description", "")
                                        create_task(conn, t["title"], desc, uid, priority)
                                        results["tasks_created"] += 1
                                    else:
                                        results["errors"].append(f"Task missing title for user {u['name']}")
                        except Exception as e:
                            results["errors"].append(f"Error creating user {u['name']}: {str(e)}")
                    else:
                        results["errors"].append(f"Invalid email for {u['name']}: {u['email']}")
                else:
                    results["errors"].append("Empty name or email")
            else:
                results["errors"].append("User missing name or email")

    if "tasks" in data:
        for t in data["tasks"]:
            if "title" in t and "user_id" in t:
                priority = t.get("priority", 3)
                desc = t.get("description", "")
                try:
                    create_task(conn, t["title"], desc, t["user_id"], priority)
                    results["tasks_created"] += 1
                except Exception as e:
                    results["errors"].append(f"Error creating task {t['title']}: {str(e)}")
            else:
                results["errors"].append("Task missing title or user_id")

    return results


if __name__ == "__main__":
    conn = setup_database()
    create_user(conn, "Alice", "alice@example.com", "admin")
    create_user(conn, "Bob", "bob@example.com", "user")
    create_task(conn, "Fix bug", "Fix the login bug", 1, 1)
    create_task(conn, "Add feature", "Add dark mode", 2, 3)
    print(format_user_report(conn))
    print(format_task_report(conn))
    conn.close()
