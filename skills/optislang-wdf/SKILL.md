---
name: optislang-wdf
description: 'Create, edit, explain or validate optiSLang Workflow Definition (.wdf) files from natural language prompts. Use this skill whenever the user wants to generate, modify, understand or validate a .wdf file, set up an optiSLang workflow, define parameters/responses, configure a Sensitivity/DOE/Optimization/Reliability workflow, or work with optiSLang components like Python nodes, MOP, Simplex, One-Click Optimization, or any ControlStatementPlugIn. Also trigger when the user mentions workflow definition language, LDL, optiSLang workflow JSON, or asks to wire up components with connections.'
argument-hint: 'Describe the workflow you want to create (e.g. "DOE with Python solver, 10 samples, 4 MaxParallel workers") or the modifications you want to make to an existing WDF file.'
---

# optiSLang Workflow Definition (WDF) Creator

WDF files are JSON documents that define optiSLang engineering workflows. They follow the Laki Definition Language (LDL) [json-schema](./json-schema).

## Quick Reference

| Element Type | `type` field | When to Use |
|---|---|---|
| Plain Component | `Component` | Non-hierarchical leaf node without location registration (e.g. MOP, Variable, Wait) |
| Connector Component | `Component` | Non-hierarchical leaf node with `registered_locations` — used as solver/integration (e.g. Python2, BatchScript, Excel) |
| Basic System | `ControlStatementPlugIn` | Hierarchical container without parametric (e.g. System, While Loop) |
| Plain Parametric System | `ControlStatementPlugIn` | Hierarchical container with `ParameterManager`/`Criteria`, but no algorithm (e.g. ParametricSystem, Reevaluate) |
| Algorithm System | `ControlStatementPlugIn` | Hierarchical parametric container that drives a DOE / optimization / reliability loop (e.g. Sensitivity, AMOP, SIMPLEX) |
| Root System | `ControlStatementPlugIn` | Mandatory outer wrapper of every WDF file (`plugInId: "RunnableSystem"`) |

See [references/osl-components.md](./references/osl-components.md) for the full element taxonomy with all `plugInId` and `source` URN values.
See [references/workflow_metadata.md](./references/workflow_metadata.md) for the global project/workflow metadata.

## File Skeleton

Every WDF starts with this skeleton. Adapt the `metadata` and `root` for the specific workflow.

**Critical:** The `root` element is ALWAYS a `ControlStatementPlugIn` with `plugInId: "RunnableSystem"`. This is the mandatory outer wrapper that every optiSLang WDF file uses — without it the file will not load. The actual algorithm systems (Sensitivity, AMOP, etc.) live inside `root.children.workflow`.

```json
{
    "metadata": {
        "agent": "GitHub Copilot",
        "description": "<human readable description>",
        "displayName": "<workflow name>",
        "typeLibrary": "urn:ansys:ldl:typelibrary:optislang:v1",
        "project_settings": {},
        "placeholder_definitions": {},
        "placeholder_mapping": {},
        "placeholder_values": {},
        "registered_files": []
    },
    "root": {
        "type": "ControlStatementPlugIn",
        "plugInId": "RunnableSystem",
        "properties": { /* see references/osl-components.md #RunnableSystem properties */ },
        "children": {
            "workflow": {
                "type": "DataDependency",
                "connections": [],
                "children": {
                    /* top-level algorithm system goes here */
                }
            }
        }
    }
}
```

## Building the Workflow Tree

### 1. Algorithm Systems (ControlStatementPlugIn)

optiSLang algorithm nodes are `ControlStatementPlugIn` elements. The `plugInId` field names the algorithm. Common values:

| Workflow Type | `plugInId` |
|---|---|
| Sensitivity / DOE | `Sensitivity` |
| MOP-based optimization | `AMOP` or `SIMPLEX` |
| One-Click Optimization | `OneClickOptimization` |
| Parametric System | `ParametricSystem` |
| Generic system | Any string (URN or plaintext) |

Each algorithm system:
- Wraps an inner **`workflow` (DataDependency)** containing the solver components.
- The inner workflow must have **`connections`** wiring `IODesign → SolverName.IDesign` and `SolverName.ODesign → IIDesign`.
- `datapins` and `inner_datapins` are **only added when the user explicitly requests them**. The full pin sets are documented in [references/osl-components.md](./references/osl-components.md) for reference.

```json
"Sensitivity": {
    "type": "ControlStatementPlugIn",
    "plugInId": "Sensitivity",
    "properties": {
        "osl_properties": {
            "JSON": {
                "MaxParallel": 4,
                "ParameterManager": {
                    "correlations": [],
                    "parameter_container": [ /* duplicate of registered_parameters with extra fields */ ]
                }
            }
        }
    },
    "children": {
        "workflow": {
            "type": "DataDependency",
            "connections": [
                { "readFrom": "IODesign", "writeTo": "SolverName.IDesign" },
                { "readFrom": "SolverName.ODesign", "writeTo": "IIDesign" }
            ],
            "children": {
                "SolverName": { /* Component definition here */ }
            }
        }
    }
}
```

### 2. Workflow Components

Workflow components are `Component` elements with a `source` URI pointing to the component type. The most common ones are documented in [references/osl-components.md](./references/osl-components.md). Connector components (e.g. Python, Excel, MATLAB, Calculator, CustomIntegration_*) have an additional `registered_locations` block defining the parameters, responses and input/output slots they register to the workflow. Registered parameters and input slots have a `locations` field defining a container of locations they are registered to. Registered responses and output slots have a `location` field defining the one location they are registered to. The location format depends on the connector component type. See [references/osl-components.md](./references/osl-components.md) for location format description of specific connector types. All registered locations have optional `reference_value` and `name` fields.

> **`Parameterize` (Text Input) location indexing:** `line` and `column` inside `input_parameter` location entries are **0-based** (first line = 0, first column = 0).

Some examples for location registrations for connector components are also available in `./references/all_nodes.wdf`.

For example, a Python connector component looks like:

```json
"MySolver": {
    "type": "Component",
    "source": "urn:ansys:optislang:component:Python2",
    "properties": {
        "osl_properties": {
            "JSON": {
                "MaxParallel": 4,
                "PythonEnvironment": "optislang python 3",
                "AutoDetectForceReal": true,
                "Source": "# python code here\n"
            }
        },
        "registered_locations": {
            "JSON": {
                "internal_variables": [],
                "registered_input_slots": [],
                "registered_output_slots": [],
                "registered_parameters": [
                    { "locations": ["x1"], "name": "x1", "reference_value": 0.0 }
                ],
                "registered_responses": [
                    { "location": "y1", "name": "y1", "reference_value": 0.0 }
                ]
            }
        }
    }
}
```

### 3. Parameters and Responses

Parameters and responses are registered in the connector components's `registered_locations.JSON`. Additional parameter configuration is done at the parent algorithm system's `ParameterManager` property.
Read [references/parametric.md](./references/parametric.md) for the full parameter type definitions (deterministic, stochastic, dependent).

### 4. Connections

Connections wire datapins between elements. Use dot-notation paths relative to the containing `DataDependency`:

```json
"connections": [
    {
        "type": "Assignment",
        "readFrom": "ComponentA.ODesign",
        "writeTo": "ComponentB.IDesign"
    }
]
```

## Procedure for Creating a WDF From a Prompt

1. **Identify the workflow type** — plain solver chain, sensitivity/DOE, optimization, reliability, or custom workflow?
2. **Identify parameters and responses** — names, types, bounds, reference values.
3. **Identify the solver/connector components for the solver chain** — Python script, calculator, Ansys tool connector, or 3rd party component? What are the registered parameters/responses/slots for each connector component?
4. **Build the tree from outside in:**
    - Start with `root` as `ControlStatementPlugIn` / `plugInId: "RunnableSystem"` with properties (see [references/osl-components.md](./references/osl-components.md)). Do **not** add `datapins` or `inner_datapins` unless the user explicitly asks for them.
    - Add `root.children.workflow` as `DataDependency` with the required inter-algorithm `connections` (even if empty for now) and a `children` dict containing all top-level nodes.
    - For multi-algorithm patterns (e.g. `Sensitivity → MOP → Optimizer`): place **all** of `Sensitivity`, `MOP`, and `Optimizer` as keys inside `root.children.workflow.children`. The inter-node connections (e.g. `Sensitivity.OParameterManager → MOP.IParameterManager`) go in `root.children.workflow.connections`.
    - Add the solver/connector `Component` (single or multiple chained) inside each algorithm's inner `workflow` DataDependency.
5. **Add inner connections** on the algorithm's inner workflow: `IODesign → SolverName.IDesign` and `SolverName.ODesign → IIDesign`. For multiple chained solvers, wire them up in sequence (e.g. `Solver1.ODesign → Solver2.IDesign`) and connect the first solver to `IODesign` and the last solver to `IIDesign`.

    **⚠ Common placement mistake:** When extending an existing single-algorithm workflow (e.g. appending `MOP` + `Optimizer` after `Sensitivity`), it is easy to accidentally add the new nodes as direct keys of the `DataDependency` object instead of inside its `children` dict. Always double-check: every named node must be inside `.children`, never a sibling of `children`.
6. **Register parameters/responses** — register parameters and responses at connector components (`registered_locations.JSON`) and configure deterministic/stochastic parameters on the algorithm system inside `osl_properties.JSON.ParameterManager.parameter_container`.
7. **Schema validation** — on demand, validate the WDF against the schema defined in [json-schema](./json-schema). "./scripts/validate.py" can be used for this. Usage: validate_workflow.py <workflow.json> <schema_directory>.

## Common Patterns

### Sensitivity / DOE with Python Solver

```
root  (ControlStatementPlugIn, plugInId: "RunnableSystem")
└── workflow  (DataDependency, connections: [])
    └── Sensitivity  (ControlStatementPlugIn, plugInId: "Sensitivity")
        └── workflow  (DataDependency)
            ├── connections: [ IODesign→Solver.IDesign, Solver.ODesign→IIDesign ]
            └── Solver  (Component, source: "urn:ansys:optislang:component:Python2")
```

### Optimization on MOP (AMOP → Optimizer / Sensitivity → MOP -> Optimizer)

AMOP → Optimizer:

```
root  (ControlStatementPlugIn, plugInId: "RunnableSystem")
└── workflow  (DataDependency)
    ├── connections: [ AMOP.OParameterManager → Optimizer.IParameterManager, AMOP.OMDBPath → Optimizer.MOP\ Solver.IMDBPath ]
    ├── AMOP (ControlStatementPlugIn, plugInId: "AMOP")
    │   └── workflow (DataDependency)
    │       ├── connections: [ IODesign → Solver.IDesign, Solver.ODesign → IIDesign ]
    │       └── Solver (Component, source: "urn:ansys:optislang:component:...")
    └── Optimizer (ControlStatementPlugIn, plugInId: "...")
        └── workflow (DataDependency)
            ├── connections: [ IODesign → MOP\ Solver.IDesign, MOP\ Solver.ODesign → IIDesign ]
            └── MOP\ Solver  (Component, source: "urn:ansys:optislang:component:Mopsolver")
```

or
Sensitivity → MOP -> Optimizer:

```
root  (ControlStatementPlugIn, plugInId: "RunnableSystem")
└── workflow  (DataDependency)
    ├── connections: [ Sensitivity.OParameterManager → MOP.IParameterManager, Sensitivity.OMDBPath → MOP.IMDBPath, MOP.OParameterManager → Optimizer.IParameterManager, MOP.OMDBPath → Optimizer.MOP\ Solver.IMDBPath ]
    ├── Sensitivity (ControlStatementPlugIn, plugInId: "Sensitivity")
    │   └── workflow (DataDependency)
    │       ├── connections: [ IODesign → Solver.IDesign, Solver.ODesign → IIDesign ]
    │       └── Solver (Component, source: "urn:ansys:optislang:component:...")
    ├── MOP (Component, source: "urn:ansys:optislang:component:MOP")
    └── Optimizer (ControlStatementPlugIn, plugInId: "")
        └── workflow (DataDependency)
            ├── connections: [ IODesign → MOP\ Solver.IDesign, MOP\ Solver.ODesign → IIDesign ]
            └── MOP\ Solver  (Component, source: "urn:ansys:optislang:component:Mopsolver")
```

If not specified, let user decide which option and which optimizer to use.
If not specified otherwise, pre-initialize parametric (`ParameterManager` and `Criteria`) properties for the optimizer from AMOP or Sensitivity parametric properties if available. Do this by adding the corresponding entries in `osl_properties.JSON` of the algorithm system.

## Important Rules

- **`root` is ALWAYS `ControlStatementPlugIn` with `plugInId: "RunnableSystem"`** — every optiSLang WDF file has this. Omitting it will cause load failures.
- **`datapins` and `inner_datapins` are omitted by default** — only add them when the user explicitly requests it. Full pin sets are in [references/osl-components.md](./references/osl-components.md).
- **Dynamic datapins** (user-defined, `"is_dynamic": true`) are added on explicit user request to any component or system.
- **`osl_properties.JSON` entries are added on demand** — only include keys that directly correspond to what the user requested (e.g. `ParameterManager`, `Source`, `PythonEnvironment`, `AlgorithmSettings`). Do NOT add boilerplate defaults (`AllowSpaceInFilePath`, `AutoSaveMode`, `RetryEnable`, `RetryCount`, `StartingDelay`, etc.) unless the user asks.
- **`project_settings` entries are added on demand** — emit `"project_settings": {}` by default. Only populate specific keys when the user asks for them (e.g. autosave, working directory, licensing). Full template is in [references/workflow_metadata.md](./references/workflow_metadata.md).
- **`registered_files` entries are added on demand** — emit `"registered_files": []` by default. Only add entries when the user explicitly names a file to register. Template is in [references/workflow_metadata.md](./references/workflow_metadata.md).
- **Placeholder (`placeholder_definitions`, `placeholder_mapping`, `placeholder_values`) entries are added on demand** — emit `"placeholder_*": {}` by default. Only add entries when the user explicitly names a placeholder to register. Template is in [references/workflow_metadata.md](./references/workflow_metadata.md).
- **Inner connections are required** — the `workflow` DataDependency inside each algorithm system must wire `IODesign → SolverName.IDesign` and `SolverName.ODesign → IIDesign` for single solver/connector components or first and last solver/connector components in a chain.
- **Component, ControlStatement and datapin names with spaces, dots or parentheses** must be escaped with `\ ` in naming and connection dot-notation paths (e.g., `One-Click\ Optimization.IDesign`).
- **`typeLibrary`** must always be `"urn:ansys:ldl:typelibrary:optislang:v1"` for optiSLang workflows.
- **`ControlStatementPlugIn`** can have at most **one** child in `children` (the inner `workflow`).
- **`DataDependency`** infers execution order from connections.
- **`DataDependency.children` is the ONLY valid container for nodes** — algorithm systems, components, and plain/parametric systems MUST always be placed inside the `.children` dict of a `DataDependency`. They MUST NOT appear as direct sibling keys of `type`, `connections`, or `children` on the `DataDependency` object itself. This applies even when appending nodes to an existing workflow (e.g. adding `MOP` and `Optimizer` after an existing `Sensitivity`). **Self-check:** After building or editing any `DataDependency`, verify its JSON shape is exactly `{ "type": "DataDependency", "connections": [...], "children": { <all nodes here> } }` with no extra keys at that level.
