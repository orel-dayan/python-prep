import socket


def run_fota_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8080))
    server.listen(5)
    print("FOTA Target Device Server running on 127.0.0.1:8080...")

    while True:
        conn, addr = server.accept()
        state = "UNAUTH"
        
        while True:
            try:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break

                cmd = data.strip()
                print(f"[HW RECV]: {cmd}")

                if cmd == "AUTH fota_pass_2026":
                    state = "IDLE"
                    conn.sendall(b"AUTH_OK\n")
                elif cmd.startswith("AUTH "):
                    conn.sendall(b"ERR_AUTH_FAILED\n")

                elif cmd.startswith("START_FLASH"):
                    if state != "IDLE":
                        conn.sendall(b"ERR_SEQUENCE\n")
                    else:
                        state = "FLASHING"
                        conn.sendall(b"READY\n")

                elif cmd.startswith("WRITE_CHUNK"):
                    if state != "FLASHING":
                        conn.sendall(b"ERR_SEQUENCE\n")
                    else:
                        conn.sendall(b"ACK\n")

                elif cmd == "FINISH_FLASH":
                    if state != "FLASHING":
                        conn.sendall(b"ERR_SEQUENCE\n")
                    else:
                        state = "IDLE"
                        conn.sendall(b"FLASH_SUCCESS: CRC_OK\n")

                else:
                    conn.sendall(f"ERR_UNKNOWN: {cmd}\n".encode())

            except Exception:
                break
                
        conn.close()

if __name__ == '__main__':
    run_fota_server()