#!/usr/bin/env python3
"""Test timeout functionality of the overlapped I/O implementation."""

import sys
import time
import threading

from ansys.optislang.core.tcp.local_socket import LocalClientSocket, LocalServerSocket, generate_local_server_id

def test_connection_timeout():
    """Test connection timeout when server doesn't exist."""
    print("Testing connection timeout...")
    
    # Try to connect to non-existent server
    non_existent_id = generate_local_server_id()
    client = LocalClientSocket()
    
    start_time = time.time()
    try:
        client.connect(non_existent_id, timeout=1.5)
        assert False, "Should have timed out"
    except (ConnectionRefusedError, TimeoutError) as e:
        elapsed = time.time() - start_time
        print(f"Connection timeout after {elapsed:.2f}s (expected ~1.5s): {e}")
        assert 1.0 <= elapsed <= 2.0, f"Timeout took {elapsed}s, expected ~1.5s"
        print("✓ Connection timeout test passed")
    finally:
        client.close()

def test_accept_timeout():
    """Test accept timeout when no client connects."""
    print("\nTesting accept timeout...")
    
    server_id = generate_local_server_id()
    server = LocalServerSocket()
    server.bind_and_listen(server_id)
    
    start_time = time.time()
    try:
        server.accept(timeout=1.5)
        assert False, "Should have timed out"
    except TimeoutError as e:
        elapsed = time.time() - start_time
        print(f"Accept timeout after {elapsed:.2f}s (expected ~1.5s): {e}")
        assert 1.0 <= elapsed <= 2.0, f"Accept timeout took {elapsed}s, expected ~1.5s"
        print("✓ Accept timeout test passed")
    finally:
        server.close()

def test_send_recv_timeout():
    """Test send/recv timeout functionality."""
    print("\nTesting send/recv timeout...")
    
    server_id = generate_local_server_id()
    server = LocalServerSocket()
    server.bind_and_listen(server_id)
    
    def slow_server():
        try:
            client, addr = server.accept(timeout=5.0)
            print("Server: Client connected, sleeping...")
            # Don't read anything, just sleep to cause client recv timeout
            time.sleep(3.0)
            client.close()
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            server.close()
    
    server_thread = threading.Thread(target=slow_server)
    server_thread.start()
    
    time.sleep(0.5)  # Let server start
    
    try:
        client = LocalClientSocket()
        client.connect(server_id, timeout=5.0)
        
        # Send data
        message = b"Hello"
        client.send(message)
        
        # Try to receive with timeout (server won't send anything)
        start_time = time.time()
        try:
            client.recv_with_timeout(1024, timeout=1.5)
            assert False, "Should have timed out"
        except TimeoutError as e:
            elapsed = time.time() - start_time
            print(f"Recv timeout after {elapsed:.2f}s (expected ~1.5s): {e}")
            assert 1.0 <= elapsed <= 2.0, f"Recv timeout took {elapsed}s, expected ~1.5s"
            print("✓ Recv timeout test passed")
        
        client.close()
        
    except Exception as e:
        print(f"Client error: {e}")
        raise
    finally:
        server_thread.join()

def test_overlapped_io_robustness():
    """Test the robustness of overlapped I/O under concurrent operations."""
    print("\nTesting overlapped I/O robustness...")
    
    server_id = generate_local_server_id()
    server = LocalServerSocket()
    server.bind_and_listen(server_id)
    
    results = []
    
    def robust_server():
        try:
            for i in range(3):
                print(f"Server: Waiting for connection {i+1}")
                client, addr = server.accept(timeout=10.0)
                print(f"Server: Accepted connection {i+1}")
                
                # Handle each client quickly with timeouts
                try:
                    data = client.recv_with_timeout(1024, timeout=2.0)
                    response = f"Response {i+1}".encode()
                    client.send_with_timeout(response, timeout=2.0)
                    results.append(i+1)
                    print(f"Server: Handled client {i+1}")
                except Exception as e:
                    print(f"Server: Error handling client {i+1}: {e}")
                finally:
                    client.close()
                    
        except Exception as e:
            print(f"Server error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            server.close()
    
    server_thread = threading.Thread(target=robust_server)
    server_thread.start()
    
    time.sleep(0.5)
    
    # Create multiple clients quickly
    client_threads = []
    
    def client_worker(client_id):
        try:
            client = LocalClientSocket()
            client.connect(server_id, timeout=5.0)
            
            message = f"Message from client {client_id}".encode()
            client.send_with_timeout(message, timeout=2.0)
            
            response = client.recv_with_timeout(1024, timeout=3.0)
            print(f"Client {client_id}: Received {response}")
            
            client.close()
            
        except Exception as e:
            print(f"Client {client_id} error: {e}")
    
    # Start multiple clients
    for i in range(3):
        thread = threading.Thread(target=client_worker, args=(i+1,))
        thread.start()
        client_threads.append(thread)
        time.sleep(0.2)  # Slight delay between clients
    
    # Wait for all clients
    for thread in client_threads:
        thread.join()
    
    server_thread.join()
    
    assert len(results) == 3, f"Expected 3 handled connections, got {len(results)}"
    print("✓ Overlapped I/O robustness test passed")

if __name__ == "__main__":
    try:
        test_connection_timeout()
        test_accept_timeout()
        test_send_recv_timeout()
        test_overlapped_io_robustness()
        print("\n🎉 All timeout tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
