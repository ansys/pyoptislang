# PyOptiSLang Workflow Authoring Skill

## 1. Skill Overview

**Skill Name:** PyOptiSLang Workflow Authoring  
**Target Library:** `ansys-optislang-core` (`pyoptislang`)

**Purpose:**  
Enable AI agents to generate correct, executable PyOptiSLang scripts for:
- Workflow construction (nodes, systems, connections, properties)
- Parametric setup (parameters, criteria, responses)
- Connector/location registration
- Safe and reproducible execution lifecycle

**Primary Interaction Model:**
- Operate on OptiSLang -> Application -> Project -> RootSystem -> Nodes hierarchy
- Modify workflows through Project -> RootSystem -> Nodes structure

**Relation to AGENTS.md:**
- `AGENTS.md` provides repository-wide constraints and high-level rules.
- `SKILL.md` provides detailed workflow-authoring behavior.
- If guidance appears inconsistent, apply the stricter rule and ask the user to clarify.

---

## 2. Core Domain Knowledge

### 2.1 Architecture Hierarchy

To access or create workflow objects, reason through:

Optislang -> Application -> Project -> RootSystem -> Nodes

- **Optislang**: session/connection entry point  
- **Application**: project management (`open`, `save`, `save_as`)  
- **Project**: execution and workflow access  
- **RootSystem**: full workflow graph  
- **Nodes**: workflow elements

**Agent rules:**
- Always operate via `Application` / `Project` public APIs.
- Do not directly instantiate internal transport-layer objects.
- Treat `RootSystem` as the top-level workflow container.

### 2.2 Workflow Structure

- Workflows are tree-structured systems of nodes.
- Core node families:
  - `Node`
  - `System`
  - `ParametricSystem`
  - `IntegrationNode`
  - `ProxySolverNode`

Inheritance reminders:
- `Node -> System -> ParametricSystem -> RootSystem`
- `Node -> IntegrationNode -> ProxySolverNode`

**Agent rules:**
- Ensure a project is loaded before workflow operations.
- Access workflow through:

```python
root_system = osl.application.project.root_system
```

### 2.3 Node Types and Responsibilities

**System / ParametricSystem**
- Containers for child nodes.
- Parametric systems provide managers:
  - `ParameterManager`
  - `CriteriaManager`
  - `ResponseManager`
  - `DesignManager`

**IntegrationNode**
- Executes workflow steps on designs.
- Typical responsibilities:
  - mapping parameter values to solver-facing locations,
  - evaluating solver logic or external tools,
  - exposing outputs as responses/variables.

**Agent rules:**
- Use node-specific APIs only for the selected node type.
- Do not transfer APIs between different node patterns without confirmation.

### 2.4 Parametric Concepts

Definitions:
- **Parameter**: input variable
- **Criteria**: objective/constraint/variable criteria
- **Response**: output value
- **Design**: one evaluated parameter set

**Agent rules:**
- Always define parametric intent explicitly.
- Use managers on the owning `ParametricSystem`.

### 2.5 Connector and Location Registration

Integration nodes expose locations for mapping workflow data.

Possible registration targets include:
- parameters
- responses
- variables
- slots

Some nodes require `load` prior to location registration.
```python
integration_node.load()
```

Some nodes support location discovery:

```python
available_input_locations = integration_node.get_available_input_locations()
available_output_locations = integration_node.get_available_output_locations()
```

**Agent rules:**
- Register locations explicitly when the node requires it.
- Use exact location and naming provided by user or confirmed examples.
- Do not guess location schema if not known.
- Missing/incorrect registration can break parameter transfer or response extraction.

### 2.6 Properties

Properties are the primary mechanism for configuring nodes and systems.

**Agent rules:**
- Do not assume property names.
- Inspect first when schema is uncertain:
  - `get_property("PropertyName")`
  - change minimal required fields
  - `set_property("PropertyName", modified_value)`
- Ask user for exact property names when not confirmed by examples/API references.

---

## 3. Clarification-First Policy (Mandatory)

PyOptiSLang contains many specialized nodes.  
If required details are missing, the agent must ask before providing final runnable code.

Mandatory clarification topics:
1. exact node type(s),
2. exact property names and target values,
3. input/output location mapping,
4. required execution policy (blocking/non-blocking, external interaction),
5. save policy and project path,
6. version constraints affecting node/property availability.

**Do not guess** node-specific APIs, property keys, or location schema.

---

## 4. Workflow Generation Patterns Using `core`

### 4.1 Standard Workflow Pattern

Typical steps:
1. Start or connect to OptiSLang.
2. Open or create project.
3. Access `RootSystem`.
4. Create systems/nodes.
5. Configure properties.
6. Register locations.
7. Connect slots where required.
8. Save project.
9. Execute project.

Template:

```python
from ansys.optislang.core import Optislang
import ansys.optislang.core.node_types as nt
from ansys.optislang.core.nodes import DesignFlow

osl = Optislang()
root = osl.application.project.root_system

system = root.create_node(type_=nt.Sensitivity, name="Study")
node = system.create_node(
    type_=nt.Python2, name="Solver", design_flow=DesignFlow.RECEIVE_SEND
)

value = node.get_property("SomeProperty")
# modify the value as needed
node.set_property("SomeProperty", value)
```

### 4.2 Parametric Workflow Structure

For studies such as Sensitivity, MOP, Optimization:

RootSystem
-> ParametricSystem
    -> Solver/Evaluation node(s)

**Agent rules:**
- Create parametric system first.
- Create study nodes inside that system.
- Configure parameters/responses/criteria at the parametric-system level unless node requires otherwise.

### 4.3 Node Placement Rules

**Agent rules:**
- Every node must be created in the system that owns its execution context.
- Solver nodes for a study belong inside that study system.
- Use RootSystem for top-level orchestration.

### 4.4 Node Connection Pattern

Connections are slot-based:

```python
node_b.get_input_slots("IDesign")[0].connect_from(node_a.get_output_slots("ODesign")[0])
```

Available slots can be inspected:

```python
for slot in node.get_input_slots():
    print(slot.name, slot.type)
for slot in node.get_output_slots():
    print(slot.name, slot.type)
```

**Agent rules:**
- Connect explicitly where required.
- Ensure slot compatibility.

### 4.5 Parametric Setup Pattern

```python
from ansys.optislang.core.project_parametric import (
    OptimizationParameter,
    ObjectiveCriterion,
    ConstraintCriterion,
    ComparisonType,
)

system.parameter_manager.modify_parameter(
    OptimizationParameter(name="X", reference_value=0.0, range=(-1.0, 1.0))
)
system.criteria_manager.add_criterion(
    ObjectiveCriterion(name="obj", expression="Y", criterion=ComparisonType.MIN)
)
system.criteria_manager.add_criterion(
    ConstraintCriterion(
        name="con",
        expression="Y",
        criterion=ComparisonType.LESSEQUAL,
        limit_expression="10.0",
    )
)
```

### 4.6 Criteria and Range Semantics

Use `ComparisonType` explicitly:
- maximize: `ComparisonType.MAX`
- minimize: `ComparisonType.MIN`
- upper bound (`<=`): `ComparisonType.LESSEQUAL`
- lower bound (`>=`): `ComparisonType.GREATEREQUAL`

Strict inequality policy:
- For `<` and `>` requests, default to non-strict representation unless user requests epsilon handling.

Range policy:
- `+-N` means `(-N, N)` around reference `0.0` unless user specifies different reference semantics.

### 4.7 Execution Lifecycle (Mandatory)

Save before execution.

Required order:
1. configure workflow,
2. save project (`save_as(...)` or user-approved save),
3. start execution (`project.start(...)`).

If save path is missing, ask user before final script output.

---

## 5. Workflow Discovery and Inspection

Existing workflows can be inspected and modified via `root_system`.

Get child nodes:

```python
children = root_system.get_nodes()
for child in children:
    print(child.name, child.type)
```

Find by name:
- Names must be unique within a single search level, but not across the entire workflow.

```python
nodes = root_system.find_node_by_name("MyNode")
```

Increase search depth when required:

```python
nodes = root_system.find_node_by_name("MyNode", search_depth=2)
```

Reverse access from node to parent system is also supported:

```python
# get direct parent system
parent = node.get_parent()
# get whole ancestor chain starting from the root system
ancestors = node.get_ancestors()
```


**Agent rules:**
- Prefer reusing existing nodes when modifying workflows.
- Verify node ownership/context before creating additional nodes.

---

## 6. Workflow Generation Using `parametric` Module

The `parametric` module provides high-level abstractions based on templates.

Recommended when user asks for template-driven study creation rather than manual node graph authoring.

### 6.1 Core Concepts

- `ParametricDesignStudyManager`
- `ParametricDesignStudy`
- `DesignStudyTemplate`

### 6.2 Standard Design Study Pattern

1. Create/connect session.
2. Ensure project context is available.
3. Create `ParametricDesignStudyManager`.
4. Define parameters/responses/criteria.
5. Define template and settings.
6. Create study.
7. Save and execute according to requested flow.

### 6.3 Minimal Example

```python
from ansys.optislang.parametric.design_study import ParametricDesignStudyManager
from ansys.optislang.parametric.design_study_templates import (
    GeneralAlgorithmTemplate,
    PythonSolverNodeSettings,
)
from ansys.optislang.core.project_parametric import OptimizationParameter, Response
import ansys.optislang.core.node_types as nt

manager = ParametricDesignStudyManager()
parameters = [OptimizationParameter(name="X", reference_value=0.0, range=(-1.0, 1.0))]
responses = [Response(name="Y", reference_value=0.0)]

template = GeneralAlgorithmTemplate(
    parameters=parameters,
    criteria=[],
    responses=responses,
    algorithm_type=nt.Sensitivity,
    solver_type=nt.Python2,
    solver_settings=PythonSolverNodeSettings(input_code="Y = X**2"),
)
study = manager.create_design_study(template=template)
```

**Agent rules:**
- Keep template settings consistent with user-requested algorithm/study type.
- Apply same clarification-first and save-before-start policy.

---

## 7. Common Failure Modes

Avoid:
1. selecting node type without confirmation,
2. setting unconfirmed property names,
3. missing or wrong location registration,
4. objective/constraint direction mismatch,
5. mixing APIs from incompatible node patterns,
6. starting project before saving,
7. creating nodes in wrong parent system.

---

## 8. Coding Rules for AI Agents

### 8.1 API usage
- Use public APIs only.
- Avoid internal transport implementation layers unless requested.

### 8.2 Style and quality
- Follow PEP8.
- Use explicit logic.
- Avoid silent assumptions.
- Use meaningful names for systems/nodes/criteria.

### 8.3 Workflow safety
- Ensure project context is valid before edits.
- Preserve existing behavior unless user requests change.

---

## 9. Pre-Delivery Checklist

Before returning runnable code, confirm:
1. node type(s) are user-confirmed,
2. property names/values are user-confirmed or source-confirmed,
3. location registration matches selected node capabilities,
4. parameter bounds and criteria match requested semantics,
5. project save step exists before execution,
6. no incompatible API mixing is present.

---

## 10. Output Quality Requirements

Generated responses must:
1. state missing information explicitly when present,
2. ask targeted clarification questions before final code when ambiguity exists,
3. explain selected node/system choices briefly,
4. provide runnable code only after required details are established.
