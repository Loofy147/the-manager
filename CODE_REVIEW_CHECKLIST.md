# Code Review Checklist

This checklist should be used for all code reviews to ensure that all contributions are held to the same high standard.

## Readability

- [ ] Is the code clear and easy to understand?
- [ ] Are variable and function names descriptive?
- [ ] Is the code well-commented, especially in complex areas?

## Tests

- [ ] Does the code have adequate unit and integration tests?
- [ ] Do the tests cover both happy paths and edge cases?
- [ ] Do all tests pass?

## Complexity

- [ ] Is the code overly complex?
- [ ] Can any of the code be simplified?
- [ ] Does the code adhere to the Single Responsibility Principle?

## Docs

- [ ] Is the code documented in the `README.md` or other relevant documentation?
- [ ] Are any new dependencies or environment variables documented?

## Security

- [ ] Does the code introduce any new security vulnerabilities?
- [ ] Are all inputs validated and sanitized?
- [ ] Are secrets handled securely?

## Performance

- [ ] Does the code introduce any performance regressions?
- [ ] Has the performance of the code been benchmarked?

## Rollback Plan

- [ ] Is there a plan for rolling back the changes if something goes wrong?
- [ ] Have the changes been tested in a staging environment?
