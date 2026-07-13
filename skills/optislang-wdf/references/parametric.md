# Parameter and Response Types

## Parameter Types

Parameters are originally declared in `registered_locations.JSON` → `registered_parameters` at connector components. The configuration of parameters takes place in the `osl_properties.JSON` → `ParameterManager` at algorithm systems. If not specified explicitly, set lower/upper bounds to -10%/+10% for continuous parameters.

```json
"ParameterManager" :
{
    "correlations" : [],
    "parameter_container" : []
}
```

### Deterministic (Continuous)

```json
{
    "active" : true,
    "const" : false,
    "deterministic_property" :
    {
        "domain_type" : "real",
        "kind" : "continuous",
        "lower_bound" : 9.0,
        "upper_bound" : 11.0
    },
    "modifiable" : false,
    "name" : "Parameter_0",
    "reference_value" : 10.0,
    "removable" : true,
    "type" : "deterministic",
    "unit" : ""
}
```

### Deterministic (Discrete / Integer)

```json
{
    "active" : true,
    "const" : false,
    "deterministic_property" :
    {
        "discrete_states" : [ 9, 10, 11 ],
        "domain_type" : "integer",
        "kind" : "ordinaldiscrete_value"
    },
    "modifiable" : false,
    "name" : "Parameter_3",
    "reference_value" : 10,
    "removable" : true,
    "type" : "deterministic",
    "unit" : ""
}
```

### Stochastic (Normal Distribution)

```json
{
    "active" : true,
    "const" : false,
    "modifiable" : false,
    "name" : "Parameter_1",
    "reference_value" : 10.0,
    "removable" : true,
    "stochastic_property" :
    {
        "cov" : 0.10000000000000001,
        "kind" : "marginaldistribution",
        "statistical_moments" : [ 10.0, 1.0 ],
        "type" : "normal"
    },
    "type" : "stochastic",
    "unit" : ""
}
```

### Dependent

```json
{
    "active" : true,
    "const" : false,
    "dependency_expression" : "Parameter_0",
    "modifiable" : false,
    "name" : "Parameter_2",
    "reference_value" : 10.0,
    "removable" : true,
    "type" : "dependent",
    "unit" : ""
}
```

## Response Types

Responses are declared in `registered_locations.JSON` → `registered_responses` at connector components. No additional configuration at algorithm systems required.

## Criteria (Objectives and Constraints)

Criteria are defined in the algorithm system's `osl_properties.JSON.Criteria.sequence` array.

Base structure:

```json
"Criteria" :
{
    "header" : 0,
    "sequence" : []
}
```

### Minimize Objective

```json
{
    "First": "obj_mass",
    "Second": {
        "rhs": "mass",
        "type": "min"
    }
}
```

### Maximize Objective

```json
{
    "First": "obj_profit",
    "Second": {
        "rhs": "profit",
        "type": "max"
    }
}
```

### Inequality Constraint (less-equal)

```json
{
    "First": "constr_stress",
    "Second": {
        "lhs": "abs(max_stress)",
        "rhs": "20000",
        "type": "lessequal"
    }
}
```

### Equality Constraint

```json
{
    "First": "constr_volume",
    "Second": {
        "lhs": "volume",
        "rhs": "100.0",
        "type": "equal"
    }
}
```
