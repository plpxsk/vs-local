# Code Review Demo

Use Continue.dev to review `examples/sample_app/app.py` for bugs and issues.

## Exercise: Full Review

Open the file and prompt:
```
Review this code for security vulnerabilities, bugs, code smells, and
suggest improvements. Prioritize by severity.
```

## Expected Findings

The model should identify:

1. **SQL Injection** (Critical) - `get_user()` and `get_user_tasks()` use string concatenation
2. **Code duplication** - `format_user_report` and `format_task_report` are nearly identical
3. **Long function** - `process_bulk_import` does too many things
4. **No connection management** - No context managers or proper cleanup
5. **Magic numbers** - Priority values, string lengths
6. **No input validation** - Functions trust all input

## Tips

- Ask for severity ratings
- Ask for fixed code examples
- Use "Explain this code" to understand unfamiliar patterns
