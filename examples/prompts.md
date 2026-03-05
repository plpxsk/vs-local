# Curated Prompt Library

Effective prompts for coding tasks with local models.

## Code Generation

### Function Implementation
```
Write a Python function called `{name}` that {description}.
Input: {input_types}
Output: {output_type}
Include type hints and a docstring.
```

### Class Design
```
Design a Python class for {concept} with:
- Attributes: {list attributes}
- Methods: {list methods}
Use dataclass if appropriate. Include __str__ and __repr__.
```

## Refactoring

### Simplify
```
Simplify this code while preserving behavior. Remove duplication,
improve naming, and reduce nesting.
```

### Extract Method
```
Extract the {description} logic into a separate function.
Name it descriptively and add type hints.
```

### Modernize
```
Update this code to use modern Python (3.10+) features:
match statements, type unions with |, walrus operator where helpful.
```

## Code Review

### Security Review
```
Review this code for security vulnerabilities (OWASP Top 10).
List each issue with severity, location, and fix.
```

### Performance Review
```
Analyze this code for performance issues. Consider time complexity,
unnecessary allocations, and I/O patterns. Suggest specific fixes.
```

## Testing

### Unit Tests
```
Write pytest tests for this function. Include:
- Happy path with typical input
- Edge cases (empty, None, boundary values)
- Error cases that should raise exceptions
Use fixtures and parametrize where appropriate.
```

### Mock External Dependencies
```
Write tests for this function that mock {dependency}.
Use pytest-mock and verify the mock was called correctly.
```

## Documentation

### Docstring
```
Write a Google-style docstring for this function including
Args, Returns, Raises, and a usage Example.
```

### README Section
```
Write a README section explaining how to use {feature}.
Include installation, configuration, and a minimal example.
```

## Tips for Better Results

1. **Be specific** - Include types, constraints, and expected behavior
2. **Provide context** - Mention the framework, library, or conventions
3. **Show examples** - Give sample input/output when possible
4. **Iterate** - Ask follow-up questions to refine the output
5. **Use selection** - Select relevant code before prompting for context
