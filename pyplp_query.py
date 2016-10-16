#!/usr/bin/python3

DB_FILE_NAME = 'pyplp_1.db' # FIXME: only for debug

from database import alchemy
		

class DbInterrogator:
	
	def __init__(self):
		pass
	
	def get_bounced(self):
		pass
		
	
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Query a pyplp database')
	parser.add_argument('type', help='Type of query')
	args = parser.parse_args()
