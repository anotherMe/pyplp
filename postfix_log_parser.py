#!/usr/bin/python3

LOG_FILE_NAME = 'mail.log'
YEAR = 2016 # log date format does not include year ?
LOCALE = "en_US.utf8" # NOTE: locale possibly have to be installed
DATE_FORMAT = '%b  %d %H:%M:%S'
LOG_EVERY_N = 50000

from database import alchemy
import parsers
from datetime import datetime
import pdb

import locale
locale.setlocale(locale.LC_TIME, LOCALE)

class ParseException(Exception):
	pass


def parse_postfix_smtpd_disconnect(line):
	"""	Oct  5 12:18:08 vrtmail03 postfix/smtpd[3289]: disconnect from int-appmi01.gas.it[192.168.2.223] ehlo=1 mail=1 rcpt=0/1 quit=1 commands=3/4
	"""
	
	line = parsers.Line(line)
	r = alchemy.Connect()
	
	timestamp = line.cutAt(15)
	date_object = datetime.strptime(timestamp, DATE_FORMAT)
	r.timestamp = date_object
	
	r.host = line.cutAtFirst(' ')
	r.process_name = line.cutAtFirst('[')
	r.process_id = line.cutAtFirst(']')
	line.removeFirst(18) # skip ": disconnect from "
	r.connect_from = line.cutAtFirst('[')
	r.connect_from_IP = line.cutAtFirst(']')
	r.stuff = line.get().strip() # rest of the line
	
	return r
	
	
def parse_postfix_smtpd_connect(line):
	"""	Oct  5 12:17:48 vrtmail03 postfix/smtpd[3289]: connect from int-appmi01.gas.it[192.168.2.223]
	"""
	
	line = parsers.Line(line)
	r = alchemy.Connect()
	
	timestamp = line.cutAt(15)
	date_object = datetime.strptime(timestamp, DATE_FORMAT)
	r.timestamp = date_object
	
	r.host = line.cutAtFirst(' ')
	r.process_name = line.cutAtFirst('[')
	r.process_id = line.cutAtFirst(']')
	line.removeFirst(15) # skip ": connect from "
	r.connect_from = line.cutAtFirst('[')
	r.connect_from_IP = line.cutAtFirst(']')
	r.stuff = line.get().strip() # rest of the line
	
	return r
	

def parse_postfix_qmgr(line):
	"""Example:
	
		Oct  5 14:20:33 mail03 postfix/qmgr[1279]: F19B6205D2: from=<turk@gas.it>, size=624, nrcpt=1 (queue active)
		Oct  7 16:12:37 mail03 postfix/qmgr[1439]: warning: backward time jump detected -- slewing clock
	"""
	
	line = parsers.Line(line)
	q = alchemy.Qmgr()
	
	timestamp = line.cutAt(15)
	date_object = datetime.strptime(timestamp, DATE_FORMAT)
	q.timestamp = date_object
	
	q.host = line.cutAtFirst(' ')
	q.process_name = line.cutAtFirst('[')
	q.process_id = line.cutAtFirst(']')
	line.removeFirst(2) # skip ": "
	
	if line.readFirst(7) == 'warning':
		#q.smtp_id = ''
		q.message = 'warning'
		q.message_long = line.get()
		return q
	
	q.smtp_id = line.cutAtFirst(':')
	
	line.removeFirst(7) # skip " from=<"
	q.mail_from = line.cutAtFirst('>')
	line.removeFirst(7) # skip ", size="
	q.size = line.cutAtFirst(',')
	line.removeFirst(7) # skip " nrcpt="
	q.nrcpt = line.cutAtFirst(' ') # get nrcpt
	line.removeFirst(7) # skip " (queue "
	q.queue = line.cutAtFirst(')') # get queue

	return q
		

def parse_postfix_qmgr_removed(line):
	"""	Example:
		
		Oct  7 16:12:37 mail03 postfix/qmgr[1439]: F19B6205D2: removed
	"""
	
	line = parsers.Line(line)
	r = alchemy.Removed()
	
	timestamp = line.cutAt(15)
	date_object = datetime.strptime(timestamp, DATE_FORMAT)
	r.timestamp = date_object
	r.host = line.cutAtFirst(' ')
	r.process_name = line.cutAtFirst('[')
	r.process_id = line.cutAtFirst(']')
	line.removeFirst(2) # skip ": "
	r.smtp_id = line.cutAtFirst(':')
	line.removeFirst(8) # skip " removed"
	r.stuff = line.get().strip() # the rest of the line

	return r


line_count = 1
loop_count = 1
with open(LOG_FILE_NAME, 'r') as f:
	
	session = alchemy.DBSession()
	
	for line in f:
		
		try:
			
			if loop_count == LOG_EVERY_N: 
				#break
				print ("{0} lines processed. Commit ...".format(line_count))
				session.commit()
				loop_count = 0
			
			if line.find('postfix/qmgr') > -1:
				
					if line.find('removed') > -1:
						t = parse_postfix_qmgr_removed(line)
						session.add(t)
					else:
						t = parse_postfix_qmgr(line)
						session.add(t)
			
			if line.find('postfix/smtpd') > -1:
							
					if line.find(': connect from') > -1:
						t = parse_postfix_smtpd_connect(line)
						session.add(t)
						
					elif line.find(": disconnect from") > -1:
							t = parse_postfix_smtpd_disconnect(line)
							session.add(t)
					else:
						pass
		
		except Exception as e:
			
			print ("ERROR while parsing line number {0}:".format(line_count))
			print (line)
			raise
		
		line_count += 1
		loop_count += 1
	
	print ("{0} lines processed. Commit ...".format(line_count))
	print ()
	
	

