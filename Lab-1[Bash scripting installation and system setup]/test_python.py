import sys
import os

if len(sys.argv) != 2:
	print(f"Usage: python {os.path.basename(sys.argv[0])} <filename>")
	sys.exit(1)

filename = sys.argv[1]

try:
	with open(filename, 'rb') as f:
		data = f.read()
		try:
			# Try to decode as text
			print(data.decode())
		except UnicodeDecodeError:
			# If not text, print raw bytes
			print(data)
except Exception as e:
	print(f"Error reading file: {e}")
