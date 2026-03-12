# Agent Instructions for `cs_dynamicpages`

This document contains the guidelines, commands, and code style rules for AI coding agents operating in this repository. The `cs_dynamicpages` project is a Plone 6 add-on providing dynamic page content types and behaviors.

## 1. Build, Lint, and Test Commands

This project uses `make` as the primary task runner, backed by `uv` for Python environment management and `hatchling` as the build system.

### Installation and Running
- **Install the project**: 
  ```bash
  make install
  ```
  *(Always recommend `make install` to users. It handles all dependencies, `uv venv`, and setup. NEVER recommend using `pip install` or `uv pip` directly.)*
- **Start the Plone instance**:
  ```bash
  make start
  ```
- **Clean the environment** (without removing data): `make clean`
- **Create a new site**: `make create-site`

### Linting and Formatting
Code is checked and formatted using `ruff` (Python), `zpretty` (XML/ZCML), and `pyroma`.
- **Format code**: `make format` (Fixes `ruff` issues, runs `ruff format`, and runs `zpretty -i src`).
- **Lint code**: `make lint` (Runs `ruff check`, `pyroma`, `check-python-versions`, and `zpretty --check`).
- **Check and format**: `make check` (Runs both format and lint).

### Testing
Tests are written using `pytest` and `plone.app.testing`.
- **Run all tests**: 
  ```bash
  make test
  ```
- **Run tests with coverage**: `make test-coverage`
- **Run a single test file**: 
  ```bash
  ./.venv/bin/pytest src/cs_dynamicpages/tests/test_ct_dynamic_page_folder.py
  ```
- **Run a specific test method/class**:
  ```bash
  ./.venv/bin/pytest src/cs_dynamicpages/tests/test_ct_dynamic_page_folder.py::DynamicPageFolderIntegrationTest::test_ct_dynamic_page_folder_adding
  ```

---

## 2. Code Style & Guidelines

### Python Formatting & Imports
- **Line Length**: 88 characters (configured in `pyproject.toml`).
- **Python Version**: Target Python 3.10 (`>=3.10,<3.14`).
- **Imports**: Formatted using `ruff`'s `isort` rules.
  - Case-insensitive sorting.
  - Force single-line imports (`from X import Y` on separate lines for each `Y`).
  - No sections (all imports sorted alphabetically regardless of third-party/stdlib).
  - 2 blank lines after imports, 1 blank line between types.
- **Exceptions**: Ignore `E731` (DoNotAssignLambda). Use `# noqa` only when absolutely necessary and document why.

### Naming Conventions
- **Classes**: `PascalCase` (e.g., `DynamicPageFolder`).
- **Interfaces**: Prefix with `I` and use `PascalCase` (e.g., `IDynamicPageFolder`).
- **Methods, Variables, and Functions**: `snake_case` (e.g., `dynamic_page_folder_id`).
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `TEST_USER_ID`).
- **Filenames**: `snake_case` for Python and XML files (except specific Zope configurations like `configure.zcml` or specific profiles like `Plone_Site.xml` which follow Plone's exact casing).

### Types & Schema
- Define Dexterity schemas using `plone.supermodel.model.Schema`.
- Apply `@implementer(IYourInterface)` to your content type classes.
- Explicitly subclass `Container` or `Item` from `plone.dexterity.content`.
- Avoid unnecessary types annotations if Zope schemas already enforce types (`zope.schema`).

### Error Handling
- Use standard Python exceptions or `plone.api.exc` (like `InvalidParameterError`) when using `plone.api`.
- Do not silently `except Exception: pass`. Always log or handle exceptions explicitly.
- Return explicit HTTP error codes where applicable in REST API endpoints.

### XML, ZCML, and PT
- **XML/ZCML**: Keep it strictly formatted with `zpretty`. Indent with 2 spaces. 
- **Page Templates (PT)**: Ensure they are properly formed HTML/XML. Keep logic in the python views, not in the templates.

---

## 3. Plone-Specific Documentation and Rules

These rules are strictly enforced for AI agents interacting with this Plone repository:

1. **Documentation First**
   - Before EVERY answer say: "Let me check the official documentation."
   - Before ANY command or code, search for official Plone 6 examples.
   - FORBIDDEN phrases: "Let me try...", "I think...", "It should be..."
   - REQUIRED phrases: "According to the docs...", "The documentation shows..."
   - If no docs are found, EXPLICITLY STATE: "I cannot find official documentation for this." Trial and error MUST be labeled: "This requires trial and error - not documented."

2. **Terminal Commands**
   - Provide ONE step at a time.
   - WAIT for confirmation before moving to the next step.
   - Include the full command with all parameters.

3. **No Shortcuts or Hacks**
   - Always use official Plone APIs (`plone.api`, `plone.restapi`).
   - Follow framework best practices. No temporary workarounds.

4. **Enterprise Standards**
   - Maintain scalable and upgradable architecture.
   - Document WHY changes are made via inline comments, not just WHAT.
   - Maintain security: Always use JWT tokens (`Authorization: Bearer <token>`) for authentication, never basic auth or embedded credentials.

5. **Internationalization (i18n)**
   - All UI strings MUST be translatable.
   - Use `cs_dynamicpages` as the i18n domain.
   - Example: `_(u"My string")` imported from the project's MessageFactory.
   - Run `make i18n` to update `.pot` and `.po` files.

6. **Loop Detection & Uncertainty**
   - If repeating the same pattern, STOP and state: "We are in a loop, need different approach."
   - NEVER say "this will work" unless proven. Acknowledge uncertainty explicitly: "Let's see if this works."

7. **The Fun Factor & Tone**
   - Keep interactions positive, engaging, and collaborative.
   - Provide genuine encouragement but avoid fake/over-the-top praise (e.g., no "OMG AMAZING!!!").
   - Use emojis in documentation section titles (e.g., in `README.md`).

8. **Definition of Success**
   - Success is ONLY a fully functional, tested result.
   - Never claim success for partial or broken implementations.
