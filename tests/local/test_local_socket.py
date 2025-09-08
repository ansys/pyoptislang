#!/usr/bin/env python3
"""
Test script for local socket implementation with timeout testing.
"""

import sys
import time
import threading

from ansys.optislang.core.tcp.local_socket import LocalClientSocket, LocalServerSocket, generate_local_server_id

def test_basic_communication():
    """Test basic local socket communication."""
    print(f"Testing basic communication on platform: {sys.platform}")
    
    # Generate server ID
    server_id = generate_local_server_id()
    print(f"Generated server ID: {server_id}")
    
    # Create server
    server = LocalServerSocket()
    server.bind_and_listen(server_id)
    print(f"Server listening on: {server_id}")
    
    def server_handler():
        try:
            server_client, addr = server.accept(timeout=5.0)
            print(f"Server accepted connection from: {addr}")
            
            # Receive data on server side
            received = server_client.recv(1024)
            print(f"Server received: {received}")
            
            # Send response back
            response = b"Server response"
            server_client.send(response)
            server_client.close()
            
        except Exception as e:
            print(f"Server handler error: {e}")
            raise
        finally:
            server.close()
    
    # Start server in thread
    import threading
    server_thread = threading.Thread(target=server_handler)
    server_thread.start()
    
    # Give server time to start
    time.sleep(0.5)
    
    try:
        # Create client
        client = LocalClientSocket()
        client.connect(server_id, timeout=5.0)
        print("Client connected successfully")
        
        # Test sending data
        test_msg = b"Hello, local socket!"
        sent = client.send(test_msg)
        print(f"Sent {sent} bytes")
        
        # Receive response
        response = client.recv(1024)
        print(f"Client received response: {response}")
        
        client.close()
        print("Basic communication test completed successfully!")
        
    except Exception as e:
        print(f"Client error: {e}")
        raise
    finally:
        server_thread.join()

def test_timeout_functionality():
    """Test timeout functionality."""
    print(f"\nTesting timeout functionality on platform: {sys.platform}")
    
    # Test connection timeout to non-existent server
    non_existent_id = generate_local_server_id()
    print(f"Testing connection timeout to non-existent server: {non_existent_id}")
    
    client = LocalClientSocket()
    try:
        start_time = time.time()
        try:
            client.connect(non_existent_id, timeout=1.0)
            print("ERROR: Connection should have timed out!")
            assert False, "Connection should have timed out"
        except (ConnectionRefusedError, TimeoutError) as e:
            elapsed = time.time() - start_time
            print(f"Connection properly timed out after {elapsed:.1f} seconds: {e}")
            
        # Test accept timeout
        print("Testing accept timeout...")
        server_id = generate_local_server_id()
        server = LocalServerSocket()
        try:
            server.bind_and_listen(server_id)
            
            start_time = time.time()
            try:
                server.accept(timeout=1.0)
                print("ERROR: Accept should have timed out!")
                assert False, "Accept should have timed out"
            except TimeoutError as e:
                elapsed = time.time() - start_time
                print(f"Accept properly timed out after {elapsed:.1f} seconds: {e}")
                
                print("Timeout functionality test completed successfully!")
                
        except Exception as e:
            print(f"Unexpected error during accept timeout test: {e}")
            raise
        finally:
            server.close()
            
    except Exception as e:
        print(f"Unexpected error during timeout test: {e}")
        raise
    finally:
        client.close()

def test_concurrent_connections():
    """Test multiple concurrent connections."""
    print(f"\nTesting concurrent connections on platform: {sys.platform}")
    
    server_id = generate_local_server_id()
    print(f"Generated server ID: {server_id}")
    
    server = LocalServerSocket()
    server_running = threading.Event()
    test_results = []
    
    def server_thread():
        """Server thread function."""
        try:
            server.bind_and_listen(server_id)
            print(f"Server listening for concurrent connections: {server_id}")
            server_running.set()
            
            # Accept multiple connections
            for i in range(3):
                try:
                    client, addr = server.accept(timeout=5.0)
                    print(f"Server accepted connection {i+1} from: {addr}")
                    
                    # Echo back the received data
                    data = client.recv(1024)
                    client.send(data)
                    client.close()
                    test_results.append(True)
                    
                except Exception as e:
                    print(f"Server error handling connection {i+1}: {e}")
                    test_results.append(False)
                    
        except Exception as e:
            print(f"Server thread error: {e}")
            test_results.append(False)
    
    # Start server thread
    server_thread_obj = threading.Thread(target=server_thread)
    server_thread_obj.start()
    
    # Wait for server to start
    server_running.wait(timeout=5.0)
    time.sleep(0.1)  # Give server a moment to be ready
    
    # Create multiple client connections
    for i in range(3):
        try:
            client = LocalClientSocket()
            client.connect(server_id, timeout=5.0)
            
            test_msg = f"Message from client {i+1}".encode()
            client.send(test_msg)
            
            response = client.recv(1024)
            if response == test_msg:
                print(f"Client {i+1} communication successful")
                test_results.append(True)
            else:
                print(f"Client {i+1} received wrong response")
                test_results.append(False)
                
            client.close()
            
        except Exception as e:
            print(f"Client {i+1} error: {e}")
            test_results.append(False)
    
    # Wait for server thread to complete
    server_thread_obj.join(timeout=10.0)
    server.close()
    
    success_count = sum(test_results)
    total_expected = 6  # 3 server accepts + 3 client communications
    
    print(f"Concurrent connections test: {success_count}/{total_expected} operations successful")
    assert success_count == total_expected, f"Expected {total_expected} successful operations, got {success_count}"
