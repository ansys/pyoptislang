# Local Socket Tests

This directory contains tests for the local domain socket implementation that enables PyOptislang to use platform-specific communication channels instead of TCP sockets.

## Test Files

### `test_simple_local_socket.py`
Basic functionality test that verifies:
- Server ID generation
- Client-server connection establishment  
- Message exchange
- Proper connection cleanup

### `test_timeout_robustness.py`
Comprehensive timeout testing that verifies:
- Connection timeout when server doesn't exist
- Accept timeout when no client connects
- Send/receive timeout functionality
- Overlapped I/O robustness under concurrent operations

### `test_local_socket.py`
Extended test suite covering:
- Basic communication
- Timeout functionality
- Concurrent connections
- Error handling

### `test_direct_local_socket.py`
Direct module import test that bypasses circular imports to test:
- Module loading
- Class instantiation
- Basic functionality

## Platform-Specific Features Tested

### Windows Named Pipes
- **Overlapped I/O**: All operations use `FILE_FLAG_OVERLAPPED` for proper async behavior
- **Security**: Pipes restricted to current user only via security descriptors
- **Timeout Handling**: Precise timeout control using `WaitForSingleObject`
- **Resource Management**: Proper cleanup of handles and event objects

### Unix Domain Sockets
- **File Permissions**: Socket files created with 0o600 (current user only)
- **Path Management**: Automatic cleanup of socket files
- **Standard Socket API**: Uses familiar socket.AF_UNIX interface

## Running Tests

From the project root directory:

```bash
# Run individual tests
python -m pytest tests/local/test_simple_local_socket.py -v
python -m pytest tests/local/test_timeout_robustness.py -v

# Run all local tests with pytest
python -m pytest tests/local/ -v

# Run all tests in the project
python -m pytest -v
```

## Integration with PyOptislang Test Suite

These tests are now properly integrated into the PyOptislang test suite:

- **No sys.path manipulation**: Tests use standard imports from `ansys.optislang.core`
- **Pytest discovery**: All tests are automatically discovered by pytest
- **Standard test structure**: Follows the same patterns as other PyOptislang tests
- **CI/CD ready**: Can be run as part of automated testing pipelines

## Requirements

- **Windows**: pywin32 >= 306 for named pipe support
- **Linux/Unix**: Standard socket library
- **Python**: 3.9+

## Test Results Expected

All tests should pass with output showing:
- Accurate timeout measurements (within ±0.5 seconds)
- Successful message exchange between client and server
- Proper resource cleanup without errors
- Platform-appropriate socket/pipe identifiers

## Notes

- Tests use `<memory at ...>` output on Windows due to Win32 API memory objects
- Timeout tests validate timing accuracy to ensure robust overlapped I/O implementation
- Concurrent tests verify the implementation can handle multiple simultaneous connections
