# PyOptiSLang – AI Agent Guide

## Purpose
This repository provides a Python API for interacting with PyOptiSLang
instances and executing parametric studies within engineering workflows.

Typical usage follows this lifecycle:
- Create or connect to an OptiSLang instance
- Open or create a project
- Interact with the project structure (systems, nodes, parameters)
- Configure workflows (e.g., parameters, criteria, responses)
- Execute studies and retrieve results

Interaction with a Project is central to most use cases. Users typically
operate on projects by modifying their structure (systems and nodes),
configuring parameters and evaluation settings, and triggering execution.

---

## Scope
This guidance applies to:
- Source code interpretation
- Source code modifications
- API design changes
- Documentation updates

---

## Public API Rules
Public API includes:
- Documented and exported user-facing APIs (for example core entry points and documented classes)
- Public methods on those user-facing APIs

Treat as implementation details unless explicitly requested:
- transport-specific modules (for example `core.tcp`)
- internal/proxy implementation classes used behind public interfaces

All public APIs MUST:
- have NumPy-style docstrings
- clearly describe behavior and intent
- align with type hints

---

## Docstring Guidelines
Docstring style and quality are validated through NumPy docstring checks in documentation tooling.

Focus on:
- semantic clarity
- explicit behavior
- complete parameter and return descriptions
- documenting raised exceptions

---

## Code Quality Guidelines
- Follow PEP8
- Maintain backward compatibility
- Avoid broad exception handling
- Prefer explicit over implicit logic

---

## Domain Concepts
The PyOptiSLang API follows a hierarchical structure:

Optislang → Application → Project → RootSystem → Nodes


### Key Modules and Entry Points

- `ansys.optislang.core/...`: Core API interfaces and functionality
- `ansys.optislang.core.tcp/...`: Transport-specific implementations
- `ansys.optislang.parametric/...`: Convenience abstractions

Primary entry points:
- `Optislang`
- `Application`
- `Project`


### Core Hierarchy

- Optislang
  - Entry point responsible for starting or connecting to an OptiSLang server instance.
  - Establishes communication with the backend and provides access to higher-level APIs.

- Application
  - Provides application-level functionality such as:
    - project management (open, save, save_as)
    - version information
  - Acts as the entry point to project-level operations.

- Project
  - Central entity representing a workflow project.
  - Provides access to:
    - project execution (start, stop, reset)
    - project status
    - evaluation of designs at project level
  - Provides access to and wraps parts of the RootSystem functionality.

- RootSystem
  - Top-level parametric system within a project.
  - Contains the full workflow graph of nodes.


### Node Hierarchy

The workflow is composed of nodes with the following inheritance structure:

- Node
  - Base class for all elements in the workflow graph.

- System (inherits from Node)
  - Can contain child nodes (composite structure).

- ParametricSystem (inherits from System)
  - Provides parametric evaluation capabilities.
  - Contains:
    - ParameterManager
    - CriteriaManager
    - ResponseManager
	  - DesignManager
  - Responsible for generating and managing designs.


- RootSystem (inherits from ParametricSystem)
  - Represents the top-level workflow system of a project.


- IntegrationNode (inherits from Node)
  - Represents executable workflow steps that operate on designs.
  - Typically receives designs from a parent ParametricSystem or predecessor nodes.
  - Can:
    - map parameter values to external representations (e.g., input files, solver settings)
    - execute external tools or solvers
    - extract responses from defined result locations
  - Supports registration of locations for parameters, variables, and responses.


Nodes can be created, configured, and connected to define workflows.


### Object Access and Creation

Objects are typically accessed and managed through their parent structures:

- Projects provide execution control and access to the root system
- Topology changes should be performed through `project.root_system` (or descendant systems)
- Systems provide method to create and/or access to child nodes (e.g., `get_nodes`, search methods, `create_node`)
- Parametric systems expose managers for:
  - parameters
  - criteria
  - responses
  - designs
- Integration nodes expose locations for parameter and response registration

Direct instantiation of internal objects is uncommon and should be avoided
unless explicitly required.

Most workflows are constructed by navigating and modifying existing structures
rather than creating standalone objects by direct communication with the server.


### Additional Notes

- All systems and nodes exist within a Project context.
- Users typically interact with high-level APIs on the Project rather than directly manipulating the RootSystem.
- Modifications to workflows involve creating, configuring, and connecting nodes within systems.


### Implementation Notes

The API uses a proxy pattern:

- Core modules mostly define interfaces and high-level abstractions
- Concrete implementations are located in transport-specific layers (e.g., `tcp` module)

When modifying code:
- Prefer working at the API/interface level unless implementation changes are required
- Be aware that modifying only interface definitions may not affect runtime behavior


### Testing Guidelines

- All public API changes must include tests
- Use pytest framework
- Prefer integration-style tests for workflow logic without excessive mocking



### Convenience Layer: Parametric Module

The `parametric` module provides higher-level abstractions for creating
and executing common workflow patterns.

Key components:

- ParametricDesignStudyManager
  - Manages multiple design studies
  - Owns or uses an Optislang instance (connects or creates)
  - Provides creation, access, and persistence of studies

- ParametricDesignStudy
  - Represents a configured study
  - Supports execution, reset, and lifecycle operations

- DesignStudyTemplate
  - Base class for workflow templates
  - Defines `create_design_study`, which generates configured studies

Notes:
- This module acts as a convenience layer to simplify common workflows
- Design study templates and settings can be prepared before server connection/project availability
- Creating, resetting, or executing a design study requires an active loaded project
- It does not strictly follow the proxy pattern used in the core API
- Particularly useful when working with complex nodes such as ProxySolverNode


### Project parametric concepts

- **Parameter**: Input variable used in evaluations
- **Criteria**: Objectives, constraints, or intermediate evaluation quantities
- **Response**: Output values obtained from evaluations
- **Design**: A single evaluation instance defined by a parameter set


### Notes for LLMs

- Most user-facing operations should go through the `Project` or higher-level APIs
- Direct interaction with low-level structures (e.g., RootSystem internals)
  should be limited unless necessary
- The API uses a proxy pattern; core modules define interfaces, while actual
  implementations may reside in transport-specific layers (e.g., TCP)
- Prefer `Application`/`Project` APIs over deprecated passthrough methods on `Optislang`

---

## LLM Optimization Goals
When modifying or generating code:
- reduce ambiguity
- prefer explicit naming
- preserve API stability
- avoid unnecessary refactoring

---

## Constraints
Do NOT:
- change docstring style (enforced externally)
- modify private APIs unless required
- introduce breaking changes