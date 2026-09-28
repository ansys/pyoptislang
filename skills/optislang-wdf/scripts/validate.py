#!/usr/bin/env python3
"""Validate optiSLang WDF files against the LDL schema."""

import json
from pathlib import Path
import sys

try:
    from jsonschema.validators import validator_for
except ImportError:
    print("ERROR: jsonschema library not found.")
    print("Install it with: pip install jsonschema")
    sys.exit(1)


def load_json(file_path):
    """Load JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_workflow(workflow_path, schema_dir):
    """Validate workflow JSON against LDL schema."""
    print(f"Loading workflow from: {workflow_path}")
    workflow = load_json(workflow_path)

    print(f"Loading schema from: {schema_dir}")
    schema_dir = Path(schema_dir)

    # Load all schema files
    schemas = {}
    for schema_file in schema_dir.glob("*.schema.json"):
        schema_data = load_json(schema_file)
        schema_name = schema_file.stem.replace(".schema", "")
        schemas[schema_name] = schema_data
        if "$id" in schema_data:
            schemas[schema_data["$id"]] = schema_data
        print(f"  Loaded schema: {schema_file.name}")

    # Load main workflow schema
    workflow_schema = schemas.get("workflow")
    if not workflow_schema:
        raise ValueError("Could not find workflow schema")

    # Get the appropriate validator class for this schema
    ValidatorClass = validator_for(workflow_schema)

    # Modern approach using registry (for jsonschema >= 4.18.0)
    try:
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT202012

        # Create resources for all schemas. Register each schema under its
        # canonical $id (when present) and keep existing local aliases such as
        # "workflow" so both URI-based and filename-based references resolve.
        resource_map = {}
        for schema_name, schema_data in schemas.items():

            if not isinstance(schema_name, str):
                continue

            resource = Resource.from_contents(schema_data, default_specification=DRAFT202012)

            # Preserve existing aliases like "workflow" / "properties".
            resource_map[schema_name] = resource

            # Also register the canonical schema identifier used by $ref
            # resolution. Do not skip http(s) URIs.
            schema_id = schema_data.get("$id")
            if isinstance(schema_id, str) and schema_id:
                resource_map[schema_id] = resource

        # Build registry

        registry = Registry().with_resources(resource_map.items())

        # Create validator with registry
        validator = ValidatorClass(workflow_schema, registry=registry)
        print(f"\n  Using validator: {ValidatorClass.__name__} with Registry")

    except ImportError:
        # Fallback only when the optional referencing package is unavailable
        print(f"\n  Using validator: {ValidatorClass.__name__} (no external $ref resolution)")
        validator = ValidatorClass(workflow_schema)

    # Validate
    print("\n" + "=" * 70)
    print("VALIDATING WORKFLOW")
    print("=" * 70)

    errors = list(validator.iter_errors(workflow))

    if errors:
        print(f"\n[FAIL] VALIDATION FAILED - {len(errors)} error(s) found:\n")
        for i, error in enumerate(errors, 1):
            path_str = " -> ".join(str(p) for p in error.path) if error.path else "(root)"
            print(f"Error {i}:")
            print(f"  Path:      {path_str}")
            print(f"  Validator: {error.validator}")
            print(f"  Message:   {error.message}")
            print()
        return False
    else:
        print("\n[PASS] VALIDATION PASSED - Workflow is schema-compliant!\n")
        return True


if __name__ == "__main__":
    # Paths
    workflow_path = None
    schema_dir = None

    # Allow command line override
    if len(sys.argv) > 1:
        workflow_path = sys.argv[1]
    if len(sys.argv) > 2:
        schema_dir = sys.argv[2]

    if not workflow_path or not schema_dir:
        print("Usage: validate.py <workflow.json> <schema_directory>")
        sys.exit(1)

    try:
        success = validate_workflow(workflow_path, schema_dir)
        sys.exit(0 if success else 1)
    except FileNotFoundError as e:
        print(f"ERROR: File not found - {e}")
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON - {e}")
        sys.exit(3)
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(4)
