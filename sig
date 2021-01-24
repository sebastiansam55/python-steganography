#!/usr/bin/python3
import re
import subprocess
import os
import sys

extension = sys.argv[1]

files = os.listdir()
for i in files:
	if extension in i:
		cmd = ["/usr/bin/identify", "-verbose", i]
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
		output = p.communicate()
		sig = re.findall(r"signature: (.*?)\\n", str(output))
		print(i, sig[0])