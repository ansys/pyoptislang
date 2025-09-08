#!/usr/bin/env python3
"""Simple test of the local socket implementation with proper imports."""

import sys
import time
import threading

from ansys.optislang.core.tcp.local_socket import LocalClientSocket, LocalServerSocket, generate_local_server_id

def test_simple_communication():
    """Test basic client-server communication."""
    print("Testing simple communication...")
    
    # Generate server ID
    server_id = generate_local_server_id()
    print(f"Generated server ID: {server_id}")
    
    # Create server
    server = LocalServerSocket()
    server.bind_and_listen(server_id)
    
    success = False
    error_msg = None
    
    def server_handler():
        nonlocal success, error_msg
        try:
            print("Server: Waiting for connection...")
            client, addr = server.accept(timeout=10.0)
            print(f"Server: Accepted connection from {addr}")
            
            # Receive data
            data = client.recv(1024)
            print(f"Server: Received data: {data}")
            
            # Send response
            response = b"Hello from server!"
            bytes_sent = client.send(response)
            print(f"Server: Sent {bytes_sent} bytes")
            
            client.close()
            success = True
            
        except Exception as e:
            error_msg = f"Server error: {e}"
            print(error_msg)
            import traceback
            traceback.print_exc()
        finally:
            server.close()
    
    # Start server in thread
    server_thread = threading.Thread(target=server_handler)
    server_thread.start()
    
    # Give server time to start
    time.sleep(1.0)
    
    try:
        # Create client and connect
        print("Client: Attempting to connect...")
        client = LocalClientSocket()
        client.connect(server_id, timeout=5.0)
        print("Client: Connected successfully")
        
        # Send message
        message = b"Hello from client!"
        bytes_sent = client.send(message)
        print(f"Client: Sent {bytes_sent} bytes")
        
        # Receive response
        response = client.recv(1024)
        print(f"Client: Received response: {response}")
        
        client.close()
        
        # Verify response
        assert response == b"Hello from server!", f"Expected 'Hello from server!', got {response}"
        
    except Exception as e:
        print(f"Client error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        server_thread.join()
    
    if error_msg:
        raise Exception(error_msg)
        
    if not success:
        raise Exception("Server did not complete successfully")
        
    print("✓ Simple communication test passed!")

if __name__ == "__main__":
    try:
        test_simple_communication()
        print("\n🎉 Test passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
