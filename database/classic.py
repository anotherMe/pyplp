#!/usr/bin/python3

DB_FILE_NAME = 'example.db'

import os
import sqlite3

class db:
	
	def __init__(self, command=None):

		if command == 'reset':
			if os.path.exists(DB_FILE_NAME):
				os.remove(DB_FILE_NAME)
			
		self.conn = sqlite3.connect(DB_FILE_NAME)
		self.c = self.conn.cursor()
		self.c.execute('''CREATE TABLE qmgr (date DATE, host TEXT, process_name TEXT, process_id REAL, smtp_id TEXT, message TEXT, message_long TEXT, mail_from TEXT, size REAL, nrcpt REAL, queue TEXT)''')
		self.conn.commit()

	def load_into_qmgr(self, values):
		self.c.execute("INSERT INTO qmgr VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", values)

	def load_into_qmgr_removed(self, values):
		self.c.execute("INSERT INTO qmgr (date, host, process_name, process_id, smtp_id, message, message_long) VALUES (?, ?, ?, ?, ?, ?, ?)", values)

	def end(self):
		self.conn.commit()
		self.conn.close()
