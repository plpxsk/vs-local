# Refactoring Demo

Use Continue.dev to refactor the sample app at `examples/sample_app/app.py`.

## Exercise 1: Extract Duplicated Report Functions

Select both `format_user_report` and `format_task_report` and prompt:
```
These two functions are nearly identical. Refactor them into a single
generic report formatter that accepts a title, column names, and data rows.
```

## Exercise 2: Break Up Long Function

Select `process_bulk_import` and prompt:
```
This function is too long and deeply nested. Refactor it into smaller,
well-named functions with clear responsibilities.
```

## Exercise 3: Fix SQL Injection

Select the `get_user` function and prompt:
```
This function has a SQL injection vulnerability. Fix it using parameterized queries.
```

## Tips

- Select code first, then use Cmd+L to chat about it
- Use Cmd+I for inline edits on selected code
- Ask the model to explain its refactoring decisions
