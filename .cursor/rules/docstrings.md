
# PyOptiSLang Docstring Rules

schema_version: 1

## Context
Docstring style and quality are validated through documentation tooling (NumPy docstring checks).

## Scope
Apply rules only to:
- documented and exported user-facing APIs
- user-facing classes and methods

Do not modify unless explicitly requested:
- internal/proxy classes
- transport-specific implementations (for example tcp layer)

## Constraints
Do not:
- change docstring style
- reformat existing docstrings unnecessarily
- rewrite already-correct docstrings

## Improvement Triggers
Improve docstrings only when needed to:
- clarify ambiguous descriptions
- make behavior explicit
- ensure parameters and return values are clearly explained
- add missing exception documentation where relevant

## Consistency Rules
- align docstrings with type hints
- use consistent terminology across modules
- avoid redundant or repeated descriptions

## LLM Writing Guidance
Prefer:
- domain-specific terminology (Project, System, Node, Design)
- wording that reflects actual API behavior

Avoid:
- vague descriptions (for example "process", "handle", "do stuff")

## Change Strategy
- make targeted improvements only
- keep diffs minimal and localized
