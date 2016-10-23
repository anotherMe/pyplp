#!/usr/bin/env python

YEAR = 2016 # log date format does not include year ?
LOCALE = 'en_US.utf8' # NOTE: locale possibly have to be installed
DATE_FORMAT = '%b  %d %H:%M:%S'
LINE_BUFFER = 20000

from database import alchemy
import parsers
from datetime import datetime
import argparse
import gzip
import pdb


import locale
locale.setlocale(locale.LC_TIME, LOCALE)

class LoadException(Exception):
	pass		

class DbLoader:
	
	def __init__(self, session, filename):
		
		self.session = session
		self.filename = filename


	def open_file(self, filename):
		"""	Check if file is gzipped.
		
			Returns an io.TextIOWrapper instance
		"""
		
		try:
			with gzip.open(filename) as f:
				f.read()

		except OSError:
			return open(filename)
			
		return gzip.open(filename, 'rt')


	def run(self):
		
		line_count = 1
		loop_count = 1
		f = self.open_file(self.filename)
		for line in f:
			
			if loop_count == LINE_BUFFER:
				
				print ('Reached line {0} - commit in progress ...'.format(line_count))
				self.session.commit()
				loop_count = 0
			
			try:
				dl.insert(line)

			except:
				print('Error while parsing line {0}'.format(line_count))
				print(line)
				raise
			
			line_count += 1
			loop_count += 1

		f.close()
				
	
	#~ def postfix_smtpd_disconnect(self, line):
		#~ '''	Oct  5 12:18:08 vrtmail03 postfix/smtpd[3289]: disconnect from int-appmi01.gas.it[192.168.2.223] ehlo=1 mail=1 rcpt=0/1 quit=1 commands=3/4
		#~ '''
#~ 
		#~ line = parsers.Line(line)
		#~ r = alchemy.Disconnect()
		#~ 
		#~ timestamp = line.cutAtPos(15)
		#~ date_object = datetime.strptime(timestamp, DATE_FORMAT)
		#~ r.timestamp = date_object.replace(year=YEAR) # TODO: year substitution should be improved
		#~ 
		#~ r.host = line.cutAt(' ')
		#~ r.process_name = line.cutAt('[')
		#~ r.process_id = line.cutAt(']')
		#~ line.removeFirst(18) # skip ': disconnect from '
		#~ r.connect_from = line.cutAt('[')
		#~ r.connect_from_IP = line.cutAt(']')
		#~ r.stuff = line.get().strip() # rest of the line
		#~ 
		#~ return r
		#~ 
		#~ 
	#~ def postfix_smtpd_connect(self, line):
		#~ '''	Oct  5 12:17:48 vrtmail03 postfix/smtpd[3289]: connect from int-appmi01.gas.it[192.168.2.223]
		#~ '''
		#~ 
		#~ line = parsers.Line(line)
		#~ r = alchemy.Connect()
		#~ 
		#~ timestamp = line.cutAtPos(15)
		#~ date_object = datetime.strptime(timestamp, DATE_FORMAT)
		#~ r.timestamp = date_object
		#~ 
		#~ r.host = line.cutAt(' ')
		#~ r.process_name = line.cutAt('[')
		#~ r.process_id = line.cutAt(']')
		#~ line.removeFirst(15) # skip ': connect from '
		#~ r.connect_from = line.cutAt('[')
		#~ r.connect_from_IP = line.cutAt(']')
		#~ r.stuff = line.get().strip() # rest of the line
		#~ 
		#~ return r
		#~ 
#~ 
	#~ def postfix_qmgr(self, line):
		#~ '''Example:
			#~ Oct  5 14:20:33 mail03 postfix/qmgr[1279]: F19B6205D2: from=<turk@gas.it>, size=624, nrcpt=1 (queue active)
			#~ Oct  7 16:12:37 mail03 postfix/qmgr[1439]: warning: backward time jump detected -- slewing clock
		#~ '''
		#~ 
		#~ line = parsers.Line(line)
		#~ q = alchemy.Qmgr()
		#~ 
		#~ timestamp = line.cutAtPos(15)
		#~ date_object = datetime.strptime(timestamp, DATE_FORMAT)
		#~ q.timestamp = date_object
		#~ 
		#~ q.host = line.cutAt(' ')
		#~ q.process_name = line.cutAt('[')
		#~ q.process_id = line.cutAt(']')
		#~ line.removeFirst(2) # skip ': '
		#~ 
		#~ if line.readFirst(7) == 'warning':
			#~ #q.smtp_id = ''
			#~ q.message = 'warning'
			#~ q.message_long = line.get()
			#~ return q
		#~ 
		#~ q.smtp_id = line.cutAt(':')
		#~ 
		#~ line.removeFirst(7) # skip ' from=<'
		#~ q.mail_from = line.cutAt('>')
		#~ line.removeFirst(7) # skip ', size='
		#~ q.size = line.cutAt(',')
		#~ line.removeFirst(7) # skip ' nrcpt='
		#~ q.nrcpt = line.cutAt(' ') # get nrcpt
		#~ line.removeFirst(7) # skip ' (queue '
		#~ q.queue = line.cutAt(')') # get queue
#~ 
		#~ return q
			#~ 
#~ 
	#~ def postfix_qmgr_removed(self, line):
		#~ '''	Example:
			#~ 
			#~ Oct  7 16:12:37 mail03 postfix/qmgr[1439]: F19B6205D2: removed
		#~ '''
		#~ 
		#~ line = parsers.Line(line)
		#~ r = alchemy.Removed()
		#~ 
		#~ timestamp = line.cutAtPos(15)
		#~ date_object = datetime.strptime(timestamp, DATE_FORMAT)
		#~ r.timestamp = date_object
		#~ r.host = line.cutAt(' ')
		#~ r.process_name = line.cutAt('[')
		#~ r.process_id = line.cutAt(']')
		#~ line.remove(': ')
		#~ r.smtp_id = line.cutAt(':')
		#~ line.remove(' removed')
		#~ r.stuff = line.get().strip() # the rest of the line
#~ 
		#~ return r


	def bounced(self, timestamp, smtp_id, status, line):
		'''	Parse bounced or deferred
			
			Example:
			
			Oct  7 16:44:50 mail03 postfix/smtp[1824]: 6050122915: to=<romaingmario@tiscali.it>, relay=etb-4.mail.tiscali.it[213.205.33.62]:25, conn_use=2, delay=0.13, delays=0.05/0/0.04/0.04, dsn=5.1.1, status=bounced (host etb-4.mail.tiscali.it[213.205.33.62] said: 550 5.1.1 <romaingmario@tiscali.it> recipient does not exist (in reply to RCPT TO command))
		'''

		r = alchemy.Bounced()
		
		r.smtp_id = smtp_id
		r.timestamp = timestamp
		
		line.remove(' to=<')
		r.mail_to = line.cutAt('>')
		line.remove(', relay=')
		r.relay = line.cutAt(',')
		if line.get()[:9] == ' conn_use':
			line.remove(' conn_use=')
			r.conn_use = line.cutAt(',')
		line.remove(' delay=')
		r.delay = line.cutAt(',')
		line.remove(' delays=')
		r.delays = line.cutAt(',')
		line.remove(' dsn=')
		r.dsn = line.cutAt(',')
		line.remove(' status=')
		line.cutAt(' ')
		r.bounce_type = status
		
		self.session.add(r)
		
		
	#~ def dump(self, line):
#~ 
		#~ line = parsers.Line(line)		
		#~ r = alchemy.Dump()
		#~ 
		#~ timestamp = line.cutAtPos(15)
		#~ date_object = datetime.strptime(timestamp, DATE_FORMAT)
		#~ r.timestamp = date_object
		#~ line.remove(' ')
		#~ r.host = line.cutAt(' ')
		#~ r.process_name = line.cutAt('[')
		#~ r.process_id = line.cutAt(']')
		#~ line.remove(': ')
		#~ r.stuff = line.get()
		#~ return r
		

	def insert(self, line_string):
		
		line = parsers.Line(line_string)
		r = alchemy.Bulk()
		
		timestamp = line.cutAtPos(15)
		date_object = datetime.strptime(timestamp, DATE_FORMAT)
		r.timestamp = date_object
		line.remove(' ')
		r.host = line.cutAt(' ')
		r.process_name = line.cutAt('[')
		r.process_id = line.cutAt(']')
		line.remove(': ')
		if line.get()[10] == ':' and line.get()[:10] != 'statistics':
			smtp_id = line.cutAt(':')
			r.smtp_id = smtp_id
			
		tmpval = line.get()
		r.stuff = tmpval
		
		if tmpval.find('status=bounced') > -1:
			b = self.bounced(date_object, smtp_id, 1, line)
			
		elif tmpval.find('status=deferred') > -1:
			self.bounced(date_object, smtp_id, 2, line)
		
		self.session.add(r)


if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='Load Postfix file into relational database')
	parser.add_argument('file', help='Postfix log file')
	args = parser.parse_args()
	
	dl = DbLoader(alchemy.DBSession(), args.file)
	dl.run()
	
