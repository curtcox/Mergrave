# Process principles

- Favor the simplest implementation that satisfies the requirement. Choose clarity over cleverness in both production code and tests so future readers can understand the intent quickly.
- Keep tests narrowly focused yet meaningful. Add or adjust tests alongside implementation changes so the suite provides confidence that green tests indicate a working application.
- Work in small, incremental steps. Begin each change by writing or updating a guiding test, make the minimal code change to satisfy it, and commit once the suite is green.
- Use green tests as permission to refactor. Pause to clean up code as you go, leaving the system simpler than you found it and ready for future change.
- Keep CI healthy. Run the fast checks locally, so pushes keep CI green.
- If a requested task is too large to complete well in one go, pause and propose a sequence of smaller, focused tasks that will reach the same outcome instead of pushing through the oversized request.

# Lightweight workflow

1. Understand the behavior you need to change.
2. Add or update the smallest high-value test that will fail without the change, favoring readability and comprehensive coverage of the behavior.
3. Implement the simplest code necessary to turn the test green.
4. With tests passing, refactor to improve clarity or structure while maintaining behavior.
5. Run the fast checks before pushing.

