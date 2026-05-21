# File handling

## Component file path handling

### Basic format

Basic format for files used by components and connector components:

```json
"path": {
    "base_path_mode": "",
    "split_path": { "head": "", "tail": "" }
}
```

### Absolute path

If not requested otherwise, split before file:

```json
"path": {
    "base_path_mode": "ABSOLUTE_PATH",
    "split_path": { "head": "/path/to/parent_directory", "tail": "file_name.extension" }
}
```

### Relative to working directory

If not requested otherwise, split before file:

```json
"path": {
    "base_path_mode": "WORKING_DIR_RELATIVE",
    "split_path": { "head": "/path/to/parent_directory", "tail": "file_name.extension" }
}
```

### Relative to project working directory (project .opd directory)

If not requested otherwise, split before file:

```json
"path": {
    "base_path_mode": "PROJECT_WORKING_DIR_RELATIVE",
    "split_path": { "head": "/path/to/parent_directory", "tail": "file_name.extension" }
}
```

### Relative to project directory (where project file is located)

If not requested otherwise, split before file:

```json
"path": {
    "base_path_mode": "PROJECT_RELATIVE",
    "split_path": { "head": "/path/to/parent_directory", "tail": "file_name.extension" }
}
```

### Relative to project reference files directory (project .opr directory)

If not requested otherwise, split before file:

```json
"path": {
    "base_path_mode": "REFERENCE_FILES_DIR_RELATIVE",
    "split_path": { "head": "/path/to/parent_directory", "tail": "file_name.extension" }
}
```