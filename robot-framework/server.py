import socket

def run_mock_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8080))
    server.listen(5)
    print("Advanced Mock Hardware Server running on 127.0.0.1:8080...")

    while True:
        conn, addr = server.accept()
        is_authenticated = False
        
        while True:
            try:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break

                command = data.strip()
                print(f"[RECV]: {command}")

                if command == "AUTH secret123":
                    is_authenticated = True
                    conn.sendall(b"AUTH_OK\n")
                
                elif command == "GET_SYS_STATUS":
                    conn.sendall(b"STATUS=OK\n")

                elif command == "READ_SENSORS":
                    if not is_authenticated:
                        conn.sendall(b"ERR_UNAUTHORIZED\n")
                    else:
                        conn.sendall(b"TEMP=24.5C;VOLT=3.3V\n")

                elif command == "DUMP_LOGS":
                    # Simulates a large multi-line stream dump
                    logs = "LOG_0: BOOT OK\nLOG_1: INIT SYS\nLOG_2: READY\n"
                    conn.sendall(logs.encode('utf-8'))

                elif command == "IDLE":
                    # Intentionally send nothing back to test client timeout behavior
                    pass

                else:
                    conn.sendall(f"ERR_UNKNOWN_CMD: {command}\n".encode('utf-8'))

            except Exception:
                break
                
        conn.close()

if __name__ == '__main__':
    run_mock_server()