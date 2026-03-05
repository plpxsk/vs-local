# Test Generation Demo

Use Continue.dev to generate tests for the sample app.

## Exercise 1: Generate Unit Tests

Select `create_user` and `create_task` functions, then prompt:
```
Generate pytest unit tests for these functions. Use an in-memory SQLite
database as a fixture. Cover happy path and edge cases.
```

## Exercise 2: Generate Security Tests

Prompt:
```
Write pytest tests that verify the SQL injection vulnerability in get_user().
Show both the exploit and a test for the fixed version using parameterized queries.
```

## Exercise 3: Generate Integration Tests

Prompt:
```
Write integration tests for process_bulk_import() that test:
- Valid JSON with users and tasks
- Invalid email addresses
- Missing required fields
- Empty input
```

## Tips

- Existing tests are at `examples/sample_app/tests/test_app.py`
- Ask for fixtures and parametrized tests
- Request both positive and negative test cases
