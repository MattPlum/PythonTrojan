## A simple implementation of a trojan malware in python with a C2 ( command and control ) server
Run server/attacker with "python3 c2-server.py"

Run client/victim with "python3 trojan.py"

Once socket connection is established, attacker is able to scan all files on the victim machine, run a keylogger, add/remove/download/view files on the victim machine.
