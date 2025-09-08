#!/usr/bin/env python3
"""Direct test of local_socket module without circular imports."""

import sys
import time
import threading

from ansys.optislang.core.tcp.local_socket import LocalClientSocket, LocalServerSocket, generate_local_server_id

def test_basic_communication():
    """Test basic client-server communication."""
    print("Testing basic communication...")
    
    # Generate server ID
    server_id = generate_local_server_id()
    print(f"Generated server ID: {server_id}")
    
    # Create server
    server = LocalServerSocket()
    server.bind_and_listen(server_id)
    
    def server_handler():
        try:
            client, addr = server.accept(timeout=5.0)
            print(f"Server: Accepted connection from {addr}")
            
            # Receive data
            data = client.recv(1024)
            print(f"Server: Received {data}")
            
            # Send response
            response = b"Hello from server!"
            client.send(response)
            print(f"Server: Sent response")
            
            client.close()
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            server.close()
    
    # Start server in thread
    server_thread = threading.Thread(target=server_handler)
    server_thread.start()
    
    # Give server time to start
    time.sleep(0.5)
    
    try:
        # Create client and connect
        client = LocalClientSocket()
        client.connect(server_id, timeout=2.0)
        print("Client: Connected")
        
        # Send message
        message = b"Hello from client!"
        bytes_sent = client.send(message)
        print(f"Client: Sent {bytes_sent} bytes")
        
        # Receive response
        response = client.recv(1024)
        print(f"Client: Received {response}")
        
        client.close()
        
        # Verify response
        assert response == b"Hello from server!", f"Expected 'Hello from server!', got {response}"
        print("✓ Basic communication test passed")
        
    except Exception as e:
        print(f"Client error: {e}")
        raise
    finally:
        server_thread.join()

def test_timeout_functionality():
    """Test timeout functionality."""
    print("\nTesting timeout functionality...")
    
    # Test connection timeout
    non_existent_id = generate_local_server_id()
    client = LocalClientSocket()
    
    start_time = time.time()
    try:
        client.connect(non_existent_id, timeout=1.0)
        assert False, "Should have timed out"
    except (ConnectionRefusedError, TimeoutError):
        elapsed = time.time() - start_time
        print(f"Connection timeout after {elapsed:.2f}s (expected ~1.0s)")
        assert 0.8 <= elapsed <= 1.5, f"Timeout took {elapsed}s, expected ~1.0s"
        print("✓ Connection timeout test passed")
    
    # Test accept timeout
    server_id = generate_local_server_id()
    server = LocalServerSocket()
    server.bind_and_listen(server_id)
    
    start_time = time.time()
    try:
        server.accept(timeout=1.0)
        assert False, "Should have timed out"
    except TimeoutError:
        elapsed = time.time() - start_time
        print(f"Accept timeout after {elapsed:.2f}s (expected ~1.0s)")
        assert 0.8 <= elapsed <= 1.5, f"Accept timeout took {elapsed}s, expected ~1.0s"
        print("✓ Accept timeout test passed")
    finally:
        server.close()

def test_concurrent_connections():
    """Test multiple concurrent connections."""
    print("\nTesting concurrent connections...")
    
    server_id = generate_local_server_id()
    server = LocalServerSocket()
    server.bind_and_listen(server_id)
    
    connections_handled = []
    
    def server_handler():
        try:
            for i in range(3):
                client, addr = server.accept(timeout=5.0)
                print(f"Server: Accepted connection {i+1}")
                
                # Handle connection in separate thread
                def handle_client(client_conn, conn_id):
                    try:
                        data = client_conn.recv(1024)
                        response = f"Response {conn_id}".encode()
                        client_conn.send(response)
                        connections_handled.append(conn_id)
                        client_conn.close()
                    except Exception as e:
                        print(f"Error handling client {conn_id}: {e}")
                
                thread = threading.Thread(target=handle_client, args=(client, i+1))
                thread.start()
                
        except Exception as e:
            print(f"Server handler error: {e}")
        finally:
            server.close()
    
    # Start server
    server_thread = threading.Thread(target=server_handler)
    server_thread.start()
    
    time.sleep(0.5)
    
    # Create multiple clients
    clients = []
    try:
        for i in range(3):
            client = LocalClientSocket()
            client.connect(server_id, timeout=2.0)
            client.send(f"Message {i+1}".encode())
            
            response = client.recv(1024)
            print(f"Client {i+1} received: {response}")
            
            client.close()
            clients.append(client)
            
        # Wait for server to finish
        server_thread.join()
        
        # Verify all connections were handled
        assert len(connections_handled) == 3, f"Expected 3 connections, handled {len(connections_handled)}"
        print("✓ Concurrent connections test passed")
        
    except Exception as e:
        print(f"Concurrent test error: {e}")
        raise

if __name__ == "__main__":
    try:
        test_basic_communication()
        test_timeout_functionality()  
        test_concurrent_connections()
        print("\n🎉 All tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
