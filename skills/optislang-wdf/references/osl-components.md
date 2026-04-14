# optiSLang Element Reference

This file documents the element taxonomy, `plugInId` / `source` values, and JSON properties for optiSLang WDF elements. WDF elements are either **Components** (non-hierarchical, `"type": "Component"`) or **ControlStatements** (hierarchical, `"type": "ControlStatementPlugIn"`).

---

## Element Taxonomy

```
WDF Elements
├── Component  ("type": "Component")
│   ├── Plain Components       — no registered_locations
│   └── Connector Components   — have registered_locations; used as solvers/integrations
│
└── ControlStatement  ("type": "ControlStatementPlugIn")
    ├── Basic Systems          — no parametric (ParameterManager / Criteria)
    ├── Parametric Systems     — can have ParameterManager and Criteria
    │   ├── Plain Parametric   — parametric only, no algorithm
    │   └── Algorithm Systems  — also parametric; drive DOE / optimization / reliability loops
    └── Root System            — mandatory outer wrapper of every WDF ("RunnableSystem")
```

---

## ControlStatements

### Root System

| Display Name | `plugInId` |
|---|---|
| (root of every WDF) | `RunnableSystem` |

Every optiSLang WDF file must have `root.plugInId = "RunnableSystem"`. The actual algorithm systems live inside `root.children.workflow`.

### Basic Systems

| Display Name | `plugInId` |
|---|---|
| System | `System` |
| While Loop | `CustomAlgorithm_while_loop` |

Basic systems have no parametric (no `ParameterManager` or `Criteria`).

### Plain Parametric Systems

| Display Name | `plugInId` |
|---|---|
| Parametric System | `ParametricSystem` |
| Reevaluate | `Reevaluate` |

Plain parametric systems can carry `ParameterManager` and `Criteria` in `osl_properties.JSON`, but are not algorithm systems.

### Algorithm Systems

Algorithm systems are also parametric systems — they always support `ParameterManager` and `Criteria`.

#### Optimizers

| Display Name | `plugInId` |
|---|---|
| ARSM | `ARSM` |
| Adaptive Multiple-Objective (AMO) | `CustomAlgorithm_DXAMO` |
| Adaptive Single-Objective (ASO) | `CustomAlgorithm_DXASO` |
| Mixed-Integer Sequential Quadratic Programming (MISQP) | `CustomAlgorithm_DXMISQP` |
| NLPQL | `NLPQLP` |
| Nature Inspired Optimization | `NOA2` |
| One-Click Optimization (OCO) | `CustomAlgorithm_OCO` |
| Probabilistic Inference for Bayesian Optimization (PI-BO) | `CustomAlgorithm_PIBO` |
| Simplex | `SIMPLEX` |

#### Sampling / DOE Algorithms

| Display Name | `plugInId` |
|---|---|
| AMOP (Adaptive MOP) | `AMOP` |
| Robustness | `Robustness` |
| Sensitivity / DOE | `Sensitivity` |

#### Reliability Algorithms

| Display Name | `plugInId` |
|---|---|
| ARSM-DS | `ReliabilityARSM` |
| Adaptive Sampling | `ReliabilityAS` |
| Directional Sampling | `ReliabilityDS` |
| FORM | `ReliabilityFORM` |
| ISPUD | `ReliabilityISPUD` |
| Plain Monte Carlo | `ReliabilityMC` |

#### Other Algorithm Systems

| Display Name | `plugInId` |
|---|---|
| Parametric Service (Experimental) | `ParametricService` |

---

## Components

### Plain Components

Plain components have no `registered_locations`. They do not act as solvers/integrations.

| Display Name | `source` URN |
|---|---|
| Compare | `urn:ansys:optislang:component:Compare` |
| Data Receive | `urn:ansys:optislang:component:PDMReceive` |
| Data Send | `urn:ansys:optislang:component:PDMSend` |
| Design Export | `urn:ansys:optislang:component:DesignExport` |
| Design Import | `urn:ansys:optislang:component:DataImport` |
| MOP | `urn:ansys:optislang:component:Mop` |
| Monitoring | `urn:ansys:optislang:component:VariantMonitoring` |
| Path | `urn:ansys:optislang:component:Path` |
| Postprocessing | `urn:ansys:optislang:component:Postprocessing` |
| Raw data export | `urn:ansys:optislang:component:DataExport` |
| Raw data import | `urn:ansys:optislang:component:DataImport` |
| String | `urn:ansys:optislang:component:String` |
| Variable | `urn:ansys:optislang:component:Variable` |
| Wait | `urn:ansys:optislang:component:Wait` |

### Connector Components

Connector components have `registered_locations` and are used as solvers or tool integrations. Location registration (`registered_parameters`, `registered_responses`, etc.) is specific to connector components.

#### Scripting / Generic Execution

| Display Name | `source` URN |
|---|---|
| Python | `urn:ansys:optislang:component:Python2` |
| Python Script | `urn:ansys:optislang:component:PythonScript` |
| Bash Script | `urn:ansys:optislang:component:BashScript` |
| Batch Script | `urn:ansys:optislang:component:BatchScript` |
| Perl Script | `urn:ansys:optislang:component:PerlScript` |
| Process | `urn:ansys:optislang:component:Process` |
| MATLAB | `urn:ansys:optislang:component:Matlab` |
| Calculator | `urn:ansys:optislang:component:CalculatorSet` |
| Abaqus Process | `urn:ansys:optislang:component:AbaqusProcess` |

#### Parameterization / Text-Based I/O

| Display Name | `source` URN |
|---|---|
| Text Input | `urn:ansys:optislang:component:Parameterize` |
| Text Output | `urn:ansys:optislang:component:ETKAsciiOutput` |
| Tagged Input | `urn:ansys:optislang:component:TaggedParametersParameterize` |
| ETK | `urn:ansys:optislang:component:ETKComplete` |

#### MOP Surrogate

| Display Name | `source` URN |
|---|---|
| MOP Solver | `urn:ansys:optislang:component:Mopsolver` |

#### Ansys Tools

| Display Name | `source` URN |
|---|---|
| Ansys APDL Input | `urn:ansys:optislang:component:AnsysAPDLParameterize` |
| Ansys LS-DYNA Input | `urn:ansys:optislang:component:LSDynaParameterize` |
| Ansys CFX-Solver | `urn:ansys:optislang:component:CustomIntegration_CFX-Solver-v3` |
| Ansys Fluent Mesher | `urn:ansys:optislang:component:CustomIntegration_Fluent_mesher` |
| Ansys Fluent Solver | `urn:ansys:optislang:component:CustomIntegration_Fluent_solver` |
| Ansys EDT | `urn:ansys:optislang:component:CustomIntegration_AEDT2` |
| Ansys EDT LSDSO | `urn:ansys:optislang:component:CustomIntegration_AEDT2_lsdso` |
| Ansys ROCKY Input | `urn:ansys:optislang:component:CustomIntegration_ROCKY_input` |
| Ansys ROCKY Output | `urn:ansys:optislang:component:CustomIntegration_ROCKY_output` |
| Ansys DCS | `urn:ansys:optislang:component:DPS` |
| Ansys HPS | `urn:ansys:optislang:component:HPS` |
| Ansys ModelCenter | `urn:ansys:optislang:component:CustomIntegration_ModelCenter` |
| Ansys Lumerical | `urn:ansys:optislang:component:CustomIntegration_Lumerical` |
| Ansys OpticStudio | `urn:ansys:optislang:component:CustomIntegration_OpticStudio` |
| Ansys Speos Core | `urn:ansys:optislang:component:CustomIntegration_SPEOSCore` |
| Ansys Speos Output | `urn:ansys:optislang:component:CustomIntegration_SPEOS_Report_Reader` |
| Ansys SimAI Training | `urn:ansys:optislang:component:CustomIntegration_SimAI_Training` |
| Ansys SimAI Upload | `urn:ansys:optislang:component:CustomIntegration_SimAI_Upload` |
| Ansys Thermal Desktop | `urn:ansys:optislang:component:CustomIntegration_ThermalDesktop` |

#### Third-Party CAD/CAE Tools

| Display Name | `source` URN |
|---|---|
| Excel | `urn:ansys:optislang:component:Excel` |
| MATLAB MAT Input | `urn:ansys:optislang:component:CustomIntegration_Matlab_mat_input` |
| MATLAB MAT Output | `urn:ansys:optislang:component:CustomIntegration_Matlab_mat_output` |
| ANSA Input | `urn:ansys:optislang:component:CustomIntegration_ANSA_input` |
| ANSA Output | `urn:ansys:optislang:component:CustomIntegration_ANSA_output` |
| AMESim Input | `urn:ansys:optislang:component:CustomIntegration_Amesim_input` |
| CAESES Input | `urn:ansys:optislang:component:CustomIntegration_CAESES_input` |
| CFturbo Input | `urn:ansys:optislang:component:CustomIntegration_CFturbo_input` |
| COMSOL | `urn:ansys:optislang:component:CustomIntegration_COMSOL2` |
| COMSOL Input | `urn:ansys:optislang:component:CustomIntegration_COMSOL2_Input` |
| COMSOL Output | `urn:ansys:optislang:component:CustomIntegration_COMSOL2_Output` |
| COMSOL Solve | `urn:ansys:optislang:component:CustomIntegration_COMSOL2_Solver` |
| CATIA | `urn:ansys:optislang:component:CustomIntegration_CAD_CATIA` |
| Creo | `urn:ansys:optislang:component:CustomIntegration_CAD_Creo` |
| Inventor | `urn:ansys:optislang:component:CustomIntegration_CAD_Inventor` |
| NX | `urn:ansys:optislang:component:CustomIntegration_CAD_NX` |
| CST Studio Suite | `urn:ansys:optislang:component:CustomIntegration_CST Studio Suite` |
| FloEFD Input | `urn:ansys:optislang:component:CustomIntegration_FloEFD_input` |
| FloEFD Output | `urn:ansys:optislang:component:CustomIntegration_FloEFD_output` |
| Flux Input | `urn:ansys:optislang:component:CustomIntegration_Flux_input` |
| GeoDict Input | `urn:ansys:optislang:component:CustomIntegration_GeoDict_input` |
| GeoDict Output | `urn:ansys:optislang:component:CustomIntegration_GeoDict_output` |
| GTSUITE Input | `urn:ansys:optislang:component:CustomIntegration_GTSUITE_input` |
| GTSUITE Output | `urn:ansys:optislang:component:CustomIntegration_GTSUITE_output` |
| IPG Automotive | `urn:ansys:optislang:component:CustomIntegration_IPG_Automotive` |
| JMAG Designer Input | `urn:ansys:optislang:component:CustomIntegration_JMAG_Designer_input` |
| JMAG Designer Output | `urn:ansys:optislang:component:CustomIntegration_JMAG_Designer_output` |
| JMAG Designer Solve | `urn:ansys:optislang:component:CustomIntegration_JMAG_Designer_solve` |
| JSON Input | `urn:ansys:optislang:component:CustomIntegration_JSON_input` |
| JSON Output | `urn:ansys:optislang:component:CustomIntegration_JSON_output` |
| KULI | `urn:ansys:optislang:component:CustomIntegration_KULI` |
| META Output | `urn:ansys:optislang:component:CustomIntegration_META_output` |
| MIDAS | `urn:ansys:optislang:component:CustomETKIntegration_MIDAS` |
| NASTRAN | `urn:ansys:optislang:component:CustomIntegration_NASTRAN` |
| NASTRAN Input | `urn:ansys:optislang:component:CustomIntegration_NASTRAN_input` |
| NASTRAN Output | `urn:ansys:optislang:component:CustomIntegration_NASTRAN_output` |
| AxSTREAM | `urn:ansys:optislang:component:CustomIntegration_AxSTREAM` |
| SimulationX | `urn:ansys:optislang:component:CustomIntegration_SimulationX_SXOA` |
| TurboOpt Input | `urn:ansys:optislang:component:CustomIntegration_TurboOPT` |
| VirtualLab Input | `urn:ansys:optislang:component:CustomIntegration_VirtualLab_input` |
| VirtualLab Output | `urn:ansys:optislang:component:CustomIntegration_VirtualLab_output` |
| multiPlas Input | `urn:ansys:optislang:component:MultiplasParameterize` |
| Data Mining | `urn:ansys:optislang:component:DataMining` |
| generate oSL3D Wrapper | `urn:ansys:optislang:component:CustomIntegration_Generate_SoS` |
| optiSLang OMDB | `urn:ansys:optislang:component:CustomIntegration_optislang_omdb` |
| PuTTY/SSH | `urn:ansys:optislang:component:CustomIntegration_PuTTY_SSH` |

---

## Datapins Reference

> **On-demand only.** Standard `datapins` and `inner_datapins` (all with `"is_dynamic": false`) are **not** added to generated WDF files by default. Add them only when the user explicitly requests it.
>
> **Dynamic datapins** (user-defined, `"is_dynamic": true`) are separate — added to any element on explicit user request.

### RunnableSystem and Algorithm-System Datapins

Both the root `RunnableSystem` and every algorithm/parametric system share the same `datapins` and `inner_datapins` sets.

### `datapins` (outer interface pins)

```json
"datapins": {
    "ICriteria":          { "additionalMetadata": { "is_dynamic": false }, "direction": "component_input",  "type": "Criterion Sequence" },
    "IParameterManager":  { "additionalMetadata": { "is_dynamic": false }, "direction": "component_input",  "type": "Parameter Manager" },
    "IReferenceDesign":   { "additionalMetadata": { "is_dynamic": false }, "direction": "component_input",  "type": "Design" },
    "IShowPPWhenAvailable": { "additionalMetadata": { "is_dynamic": false }, "direction": "component_input", "type": "Bool" },
    "IStartDesigns":      { "additionalMetadata": { "is_dynamic": false }, "direction": "component_input",  "type": "Design Container" },
    "OBestDesigns":       { "additionalMetadata": { "is_dynamic": false }, "direction": "component_result", "type": "Design Container" },
    "OBinFilePath":       { "additionalMetadata": { "is_dynamic": false }, "direction": "component_result", "type": "Path" },
    "OCriteria":          { "additionalMetadata": { "is_dynamic": false }, "direction": "component_result", "type": "Criterion Sequence" },
    "ODesigns":           { "additionalMetadata": { "is_dynamic": false }, "direction": "component_result", "type": "Design Container" },
    "OMDBPath":           { "additionalMetadata": { "is_dynamic": false }, "direction": "component_result", "type": "Path" },
    "OParameterManager":  { "additionalMetadata": { "is_dynamic": false }, "direction": "component_result", "type": "Parameter Manager" },
    "OReferenceDesign":   { "additionalMetadata": { "is_dynamic": false }, "direction": "component_result", "type": "Design" },
    "OSuccess":           { "additionalMetadata": { "is_dynamic": false }, "direction": "component_result", "type": "Bool" },
    "OWorkingDirectories": { "additionalMetadata": { "is_dynamic": false }, "direction": "component_result", "type": "Designpoint" },
    "enabled_state":      { "additionalMetadata": { "is_dynamic": false }, "direction": "component_input",  "type": "Bool" }
}
```

### `inner_datapins` (Design routing through the inner workflow)

```json
"inner_datapins": {
    "IIDesign":          { "additionalMetadata": { "is_dynamic": false }, "direction": "control_statement_to_component",   "type": "Design" },
    "IOCriteria":        { "additionalMetadata": { "is_dynamic": false }, "direction": "control_statement_from_component", "type": "Criterion Sequence" },
    "IODesign":          { "additionalMetadata": { "is_dynamic": false }, "direction": "control_statement_from_component", "type": "Design" },
    "IOParameterManager": { "additionalMetadata": { "is_dynamic": false }, "direction": "control_statement_from_component", "type": "Parameter Manager" },
    "IOWorkingDir":      { "additionalMetadata": { "is_dynamic": false }, "direction": "control_statement_from_component", "type": "Path" }
}
```

### Inner workflow connections (required)

Inside each algorithm system's `children.workflow` DataDependency, always include:

```json
"connections": [
    { "readFrom": "IODesign",          "writeTo": "SolverName.IDesign" },
    { "readFrom": "SolverName.ODesign", "writeTo": "IIDesign" }
]
```

---

## Connector Component Properties

### Most Ansys and Third-Party CAD/CAE Tools (all `urn:ansys:optislang:component:CustomIntegration_*`) — `osl_properties.JSON`

> **On-demand only.** Only include keys the user explicitly requested or those strictly required, except for `Path`, for specifying the Anysy or 3rd party file to load.

```json
"Path" :
{
    "path" :
    {
        "base_path_mode" : "ABSOLUTE_PATH",
        "split_path" : "split_path": { "head": "/path/to/dir", "tail": "file_name.extension" }
    }
}
```

### Python (`Python2`) — `osl_properties.JSON`

> **On-demand only.** Only include keys the user explicitly requested or those strictly required, except for `Source` or `Path`, for specifying either inline Python script source, or external Python file.

**Inline script** (embed Python code directly):

```json
{
    "Source": "# inline python script\n"
}
```

**File reference** (point to an external `.py` file):

```json
{
    "Path": {
        "path": {
            "base_path_mode": "ABSOLUTE_PATH",
            "split_path": { "head": "/path/to/dir", "tail": "script.py" }
        }
    }
}
```

### Text Input (`Parameterize`) — `osl_properties.JSON`

> **0-based indexing.** In `registered_parameters` and `registered_input_slots` location entries for `Parameterize`, both `line` and `column` are **0-based** (first line = 0, first column = 0).

Text Input (`Parameterize`) writes parameter values to a file:

```json
"FilePath" : {
    "path" :
    {
        "base_path_mode" : "ABSOLUTE_PATH",
        "split_path" :
        {
            "head" : "",
            "tail" : ""
        }
    }
}
```

### Text Output (`ETKAsciiOutput`, `ETK`) — `osl_properties.JSON`


Text Output reads variables from a file written by the solver:

```json
"ImportedFiles": [
    {
        "data_type": "text_output",
        "file": {
            "path": {
                "base_path_mode": "WORKING_DIR_RELATIVE",
                "split_path": { "head": "/path/to/parent_directory", "tail": "file_name.extension" }
            }
        }
    }
]
```

### Batch/Bash/Python/Perl Script (`BatchScript` / `BashScript` / `PythonScript` / `PerlScript`) — `osl_properties.JSON`

> **On-demand only.** Only include keys the user explicitly requested or those strictly required, except for `Content` or `ScriptPath`, for specifying either inline script source, or external file.

**Inline script** (embed Python code directly):

```json
{
    "Content": "inline script"
}
```

**File reference** (point to an external file):

```json
{
    "ScriptPath": {
        "path": {
            "base_path_mode": "ABSOLUTE_PATH",
            "split_path": { "head": "/path/to/dir", "tail": "script" }
        }
    }
}
```

**Environment**

```json
{
    "Environment": [ "name=value" ]
}
```

### Excel (`Excel`) — `osl_properties.JSON`

**File reference** (point to an external file):

```json
"FilePath" : {
    "path" :
    {
        "base_path_mode" : "ABSOLUTE_PATH",
        "split_path" :
        {
            "head" : "",
            "tail" : ""
        }
    }
}
```

---

## Connector Component Location Registration

### General

`registered_locations` on a connector component must always include these 5 arrays (some can be empty):

```json
"registered_locations": {
    "JSON": {
        "internal_variables": [],
        "registered_input_slots": [
            { "locations": [...], "name": "input_slot_name", "reference_value": 1.0 }
        ],
        "registered_output_slots": [
            { "location": ..., "name": "output_slot_name", "reference_value": 0.0 }
        ],
        "registered_parameters": [
            { "locations": [...], "name": "parameter_name", "reference_value": 1.0 }
        ],
        "registered_responses": [
            { "location": ..., "name": "response_name", "reference_value": 0.0 }
        ]
    }
}
```

The format of locations inside `location` and `locations` depend on the connector component type. Some common types follow.

### Most Ansys and Third-Party CAD/CAE Tools (all `urn:ansys:optislang:component:CustomIntegration_*`)

```json
"registered_locations" :
{
    "JSON" :
    {
        "internal_variables" : [],
        "registered_input_slots" : [],
        "registered_output_slots" : [],
        "registered_parameters" :  [
            { "locations" : [ { "dir" : "input", "name" : "X2" } ], "name" : "X2", "reference_value" : 1.0 },
            { "locations" : [ { "dir" : "input", "name" : "X3" } ], "name" : "X3", "reference_value" : 1.0 }
        ],
        "registered_responses" : [
            { "location" : { "dir" : "output", "name" : "Y" }, "name" : "Y", "reference_value" : 6.5 }
        ]
    }
}
```

### Python (`Python2`)

```json
"registered_locations": {
    "JSON": {
        "internal_variables": [],
        "registered_input_slots": [],
        "registered_output_slots": [],
        "registered_parameters": [
            { "locations": ["x1"], "name": "x1", "reference_value": 1.0 }
        ],
        "registered_responses": [
            { "location": "y1", "name": "y1", "reference_value": 0.0 }
        ]
    }
}
```

### Calculator (`urn:ansys:optislang:component:CalculatorSet`)

The calculator expressions are stored in the `internal_variables` entry.

```json
"registered_locations" :
{
    "JSON" :
    {
        "internal_variables" : [
            { "created_implicitly" : false, "description" : "", "id" : "variable_1", "location" : { "expression" : "a+b", "id" : "variable_1" }, "reference_value" : { "kind" : "scalar", "scalar" : { "imag" : 0.0, "real" : 0.0 } } }
        ],
        "registered_input_slots" : [],
        "registered_output_slots" : [],
        "registered_parameters" : [
            { "locations" : [ "a" ], "name" : "a", "reference_value" : 0.0 },
            {  "locations" : [ "b" ], "name" : "b", "reference_value" : 0.0 }
        ],
        "registered_responses" : [
            { "location" : { "expression" : "a+b", "id" : "variable_1" }, "name" : "variable_1", "reference_value" : { "kind" : "scalar", "scalar" : { "imag" : 0.0, "real" : 0.0 } } }
        ]
    }
}
```

### Text Input (`Parameterize`)

Text Input (`Parameterize`) locations are specified using `line` and `column` values for the loaded input file along with some additional attributes like output `format` (`line` and `column` counting starts at 0):

```json
"registered_locations" :
{
    "JSON" :
    {
        "internal_variables" : [],
        "registered_input_slots" : [],
        "registered_output_slots" : [],
        "registered_parameters" :
        [
            {
                "locations" : [
                    { "input_parameter" : { "column" : 20, "expandable" : true, "format" : "%18.16lf", "length" : 8, "line" : 24, "marker" : "", "name" : "Parameter_01", "preferred_format" : false, "stop_at_line_end" : true }, "type" : "input_parameter" }
                ],
                "name" : "Parameter_01",
                "reference_value" : 10.0
            },
            {
                "locations" :  [
                    { "input_parameter" : { "column" : 20, "expandable" : true, "format" : "%18.16lf", "length" : 8, "line" : 25, "marker" : "", "name" : "Parameter_02", "preferred_format" : false, "stop_at_line_end" : true }, "type" : "input_parameter" }
                ],
                "name" : "Parameter_02",
                "reference_value" : 10.0
            }
        ],
        "registered_responses" : []
    }
}
```

### Text Output (`ETK`, `ETKAsciiOutput`)

Text Output (`ETK`) locations are specified using (repeated) markers. In the example, "Mass" is a non-reapeated and "Stress" is an repeated marker:

```json
"registered_locations" :
{
    "JSON" :
    {
        "internal_variables" : [],
        "registered_input_slots" : [],
        "registered_output_slots" : [],
        "registered_parameters" : [],
        "registered_responses" :
        [
            {
                "location" :
                {
                    "etk_variable" :
                    {
                        "type" : "etk_ascii_output_variable",
                        "variable" :
                        {
                            "base_path" : "/path/to/directory",
                            "encoding" : "utf-8",
                            "expression" : "",
                            "file_path" : "file_name",
                            "id" : "",
                            "prefer_signal" : true,
                            "reader" :
                            {
                                "marker" :
                                {
                                    "end_search" : "Mass",
                                    "end_search_is_regex" : false,
                                    "next" :
                                    {
                                        "marker" :
                                        {
                                            "next" :
                                            {
                                                "marker" :
                                                {
                                                    "repeater" :
                                                    {
                                                        "repeater" :
                                                        {
                                                            "increment" : 1,
                                                            "max_increment" : 1,
                                                            "offset" : 0
                                                        },
                                                        "type" : "increment_repeater"
                                                    },
                                                    "separator" : " \t"
                                                },
                                                "type" : "token_reader"
                                            },
                                            "repeater" :
                                            {
                                                "repeater" :
                                                {
                                                    "increment" : 1,
                                                    "max_increment" : 1,
                                                    "offset" : 1
                                                },
                                                "type" : "increment_repeater"
                                            }
                                        },
                                        "type" : "line_reader"
                                    },
                                    "repeater" :
                                    {
                                        "repeater" :
                                        {
                                            "increment" : 1,
                                            "max_increment" : 1,
                                            "offset" : 0
                                        },
                                        "type" : "increment_repeater"
                                    },
                                    "search" : "Mass",
                                    "search_is_regex" : false
                                },
                                "type" : "regex_searcher"
                            }
                        }
                    },
                    "file_path" :
                    {
                        "path" :
                        {
                            "base_path_mode" : "WORKING_DIR_RELATIVE",
                            "split_path" :
                            {
                                "head" : "/path/to/directory",
                                "tail" : "file_name"
                            }
                        }
                    }
                },
                "name" : "Mass",
                "reference_value" :
                {
                    "kind" : "scalar",
                    "scalar" :
                    {
                        "imag" : 0.0,
                        "real" : 4196.4675299999999
                    }
                }
            },
            {
                "location" :
                {
                    "etk_variable" :
                    {
                        "type" : "etk_ascii_output_variable",
                        "variable" :
                        {
                            "base_path" : "/path/to/directory",
                            "encoding" : "utf-8",
                            "expression" : "",
                            "file_path" : "file_name",
                            "id" : "",
                            "prefer_signal" : true,
                            "reader" :
                            {
                                "marker" :
                                {
                                    "end_search" : "Stress",
                                    "end_search_is_regex" : false,
                                    "next" :
                                    {
                                        "marker" :
                                        {
                                            "next" :
                                            {
                                                "marker" :
                                                {
                                                    "repeater" :
                                                    {
                                                        "repeater" :
                                                        {
                                                            "increment" : 1,
                                                            "max_increment" : 1,
                                                            "offset" : 0
                                                        },
                                                        "type" : "increment_repeater"
                                                    },
                                                    "separator" : " \t"
                                                },
                                                "type" : "token_reader"
                                            },
                                            "repeater" :
                                            {
                                                "repeater" :
                                                {
                                                    "increment" : 1,
                                                    "max_increment" : 1,
                                                    "offset" : 1
                                                },
                                                "type" : "increment_repeater"
                                            }
                                        },
                                        "type" : "line_reader"
                                    },
                                    "repeater" :
                                    {
                                        "repeater" :
                                        {
                                            "increment" : 1,
                                            "max_increment" : 18446744073709551615,
                                            "offset" : 0
                                        },
                                        "type" : "increment_repeater"
                                    },
                                    "search" : "Stress",
                                    "search_is_regex" : false
                                },
                                "type" : "regex_searcher"
                            }
                        }
                    },
                    "file_path" :
                    {
                        "path" :
                        {
                            "base_path_mode" : "WORKING_DIR_RELATIVE",
                            "split_path" :
                            {
                                "head" : "/path/to/directory",
                                "tail" : "file_name"
                            }
                        }
                    }
                },
                "name" : "Stress",
                "reference_value" :
                {
                    "kind" : "vector",
                    "vector" : "[10]((19536.5,0),(4012.46,0),(-20463.5,0),(-5987.54,0),(3548.96,0),(4012.46,0),(14797.6,0),(-13486.6,0),(8467.66,0),(-5674.48,0))"
                }
            }
        ]
    }
}
```

### Excel (`Excel`)

Excel (`Excel`) locations are specified using sheet, row and column values or Name Manager ID (`managed_name`):

```json
"registered_locations" :
{
    "JSON" :
    {
        "internal_variables" : [],
        "registered_input_slots" : [],
        "registered_output_slots" : [],
        "registered_parameters" :
        [
            {
                "locations" :
                [
                    {
                        "managed_name" : "",
                        "max_col" : 1,
                        "max_row" : 0,
                        "min_col" : 1,
                        "min_row" : 0,
                        "sheet" : "Sheet1"
                    }
                ],
                "name" : "Parameter_01",
                "reference_value" : 10.0
            },
            {
                "locations" :
                [
                    {
                        "managed_name" : "",
                        "max_col" : 2,
                        "max_row" : 0,
                        "min_col" : 2,
                        "min_row" : 0,
                        "sheet" : "Sheet1"
                    }
                ],
                "name" : "Parameter_02",
                "reference_value" : 10.0
            }
        ],
        "registered_responses" :
        [
            {
                "location" :
                {
                    "managed_name" : "",
                    "max_col" : 1,
                    "max_row" : 2,
                    "min_col" : 1,
                    "min_row" : 2,
                    "sheet" : "Sheet1"
                },
                "name" : "Mass",
                "reference_value" : 4196.4675299999999
            }
        ]
    }
}
```

---
