# Code Generation Demo

Use Continue.dev chat (Cmd+L / Ctrl+L) with your local model to generate code.

## Example: CSV Parser

Prompt:
```
Write a Python function that parses a CSV file and returns a list of dictionaries,
where each dictionary represents a row with column headers as keys.
Handle quoted fields and custom delimiters.
```

## Example: REST API Endpoint

Prompt:
```
Write a FastAPI endpoint that accepts a JSON payload with "title" and "content" fields,
validates the input, and returns a created resource with an auto-generated ID.
```

## Example: Data Class

Prompt:
```
Create a Python dataclass called "Transaction" with fields: id (UUID), amount (Decimal),
currency (str), timestamp (datetime), and status (enum: pending, completed, failed).
Include validation and a method to convert to dict.
```

## Tips

- Be specific about types, error handling, and edge cases
- Mention the framework or library you want to use
- Ask for docstrings and type hints if needed
- Use inline edit (Cmd+I / Ctrl+I) to generate code directly in your file
