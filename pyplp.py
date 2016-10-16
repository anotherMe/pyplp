#!/usr/bin/python3

LOG_FILE_NAME = 'mail.log'
YEAR = 2016 # log date format does not include year ?
LOCALE = "en_US.utf8" # NOTE: locale possibly have to be installed
DATE_FORMAT = '%b  %d %H:%M:%S'
LOG_EVERY_N = 20000

from database import alchemy
import parsers
from datetime import datetime

import locale
locale.setlocale(locale.LC_TIME, LOCALE)


class DbLoader:
	
	def __init__(self):
		pass
	
	def postfix_smtpd_disconnect(self, line):
		"""	Oct  5 12:18:08 vrtmail03 postfix/smtpd[3289]: disconnect from int-appmi01.gas.it[192.168.2.223] ehlo=1 mail=1 rcpt=0/1 quit=1 commands=3/4
		"""
		
		line = parsers.Line(line)
		r = alchemy.Disconnect()
		
		timestamp = line.cutAtPos(15)
		date_object = datetime.strptime(timestamp, DATE_FORMAT)
		r.timestamp = date_object.replace(year=YEAR) # TODO: year substitution should be improved
		
		r.host = line.cutAt(' ')
		r.process_name = line.cutAt('[')
		r.process_id = line.cutAt(']')
		line.removeFirst(18) # skip ": disconnect from "
		r.connect_from = line.cutAt('[')
		r.connect_from_IP = line.cutAt(']')
		r.stuff = line.get().strip() # rest of the line
		
		return r
		
		
	def postfix_smtpd_connect(self, line):
		"""	Oct  5 12:17:48 vrtmail03 postfix/smtpd[3289]: connect from int-appmi01.gas.it[192.168.2.223]
		"""
		
		line = parsers.Line(line)
		r = alchemy.Connect()
		
		timestamp = line.cutAtPos(15)
		date_object = datetime.strptime(timestamp, DATE_FORMAT)
		r.timestamp = date_object
		
		r.host = line.cutAt(' ')
		r.process_name = line.cutAt('[')
		r.process_id = line.cutAt(']')
		line.removeFirst(15) # skip ": connect from "
		r.connect_from = line.cutAt('[')
		r.connect_from_IP = line.cutAt(']')
		r.stuff = line.get().strip() # rest of the line
		
		return r
		

	def postfix_qmgr(self, line):
		"""Example:
			Oct  5 14:20:33 mail03 postfix/qmgr[1279]: F19B6205D2: from=<turk@gas.it>, size=624, nrcpt=1 (queue active)
			Oct  7 16:12:37 mail03 postfix/qmgr[1439]: warning: backward time jump detected -- slewing clock
		"""
		
		line = parsers.Line(line)
		q = alchemy.Qmgr()
		
		timestamp = line.cutAtPos(15)
		date_object = datetime.strptime(timestamp, DATE_FORMAT)
		q.timestamp = date_object
		
		q.host = line.cutAt(' ')
		q.process_name = line.cutAt('[')
		q.process_id = line.cutAt(']')
		line.removeFirst(2) # skip ": "
		
		if line.readFirst(7) == 'warning':
			#q.smtp_id = ''
			q.message = 'warning'
			q.message_long = line.get()
			return q
		
		q.smtp_id = line.cutAt(':')
		
		line.removeFirst(7) # skip " from=<"
		q.mail_from = line.cutAt('>')
		line.removeFirst(7) # skip ", size="
		q.size = line.cutAt(',')
		line.removeFirst(7) # skip " nrcpt="
		q.nrcpt = line.cutAt(' ') # get nrcpt
		line.removeFirst(7) # skip " (queue "
		q.queue = line.cutAt(')') # get queue

		return q
			

	def postfix_qmgr_removed(self, line):
		"""	Example:
			
			Oct  7 16:12:37 mail03 postfix/qmgr[1439]: F19B6205D2: removed
		"""
		
		line = parsers.Line(line)
		r = alchemy.Removed()
		
		timestamp = line.cutAtPos(15)
		date_object = datetime.strptime(timestamp, DATE_FORMAT)
		r.timestamp = date_object
		r.host = line.cutAt(' ')
		r.process_name = line.cutAt('[')
		r.process_id = line.cutAt(']')
		line.remove(": ")
		r.smtp_id = line.cutAt(':')
		line.remove(" removed")
		r.stuff = line.get().strip() # the rest of the line

		return r

	def bounced(self, line):
		"""	Example:
			Oct  7 15:51:37 mail03 postfix/smtp[2876]: A63C2228B8: to=<paolonews@katamail.com>, relay=cmgw-km-2.mail.tiscali.it[213.205.35.84]:25, delay=0.66, delays=0.41/0.01/0.08/0.16, dsn=5.1.1, status=bounced (host cmgw-km-2.mail.tiscali.it[213.205.35.84] said: 550 5.1.1 <paolonews@katamail.com> recipient does not exist (in reply to RCPT TO command))
			Oct  7 15:51:41 mail03 postfix/smtp[2876]: 3EED5228B9: to=<biancogi10@gbianco.191.it>, relay=none, delay=0.55, delays=0.55/0/0.01/0, dsn=5.4.4, status=bounced (Host or domain name not found. Name service error for name=gbianco.191.it type=AAAA: Host not found)
			Oct  7 16:44:50 mail03 postfix/smtp[1824]: 6050122915: to=<romaingmario@tiscali.it>, relay=etb-4.mail.tiscali.it[213.205.33.62]:25, conn_use=2, delay=0.13, delays=0.05/0/0.04/0.04, dsn=5.1.1, status=bounced (host etb-4.mail.tiscali.it[213.205.33.62] said: 550 5.1.1 <romaingmario@tiscali.it> recipient does not exist (in reply to RCPT TO command))
		"""

		line = parsers.Line(line)
		r = alchemy.Bounced()
		
		timestamp = line.cutAtPos(15)
		date_object = datetime.strptime(timestamp, DATE_FORMAT)
		r.timestamp = date_object
		r.host = line.cutAt(' ')
		r.process_name = line.cutAt('[')
		r.process_id = line.cutAt(']')
		line.remove(": ")
		r.smtp_id = line.cutAt(':')
		line.remove(" to=<")
		r.mail_to = line.cutAt('>')
		line.remove(", relay=")
		r.relay = line.cutAt(',')
		if line.get()[:9] == " conn_use":
			line.remove(" conn_use=")
			r.conn_use = line.cutAt(",")
		line.remove(" delay=")
		r.delay = line.cutAt(",")
		line.remove(" delays=")
		r.delays = line.cutAt(",")
		line.remove(" dsn=")
		r.dsn = line.cutAt(",")
		line.remove(" status=bounced ")
		r.stuff = line.get()
		return r
		
	def to_bulk(self, line):
		
		line = parsers.Line(line)
		r = alchemy.Bulk()
		
		timestamp = line.cutAtPos(15)
		date_object = datetime.strptime(timestamp, DATE_FORMAT)
		r.timestamp = date_object
		line.remove(' ')
		r.host = line.cutAt(' ')
		r.process_name = line.cutAt('[')
		r.process_id = line.cutAt(']')
		line.remove(": ")
		if line.get()[10] == ':':
			r.smtp_id = line.cutAt(':')
		#~ elif line.get()[:7] == 'connect':
			#~ r.connect = True
		#~ elif line.get()[:10] == 'disconnect':	
			#~ r.connect = False
		r.stuff = line.get()
		return r
			
	def dump(self, line):
		
		line = parsers.Line(line)
		r = alchemy.Dump()
		
		timestamp = line.cutAtPos(15)
		date_object = datetime.strptime(timestamp, DATE_FORMAT)
		r.timestamp = date_object
		line.remove(' ')
		r.host = line.cutAt(' ')
		r.process_name = line.cutAt('[')
		r.process_id = line.cutAt(']')
		line.remove(": ")
		#~ line.code = code
		r.stuff = line.get()
		return r



if __name__ == "__main__":
	
	line_count = 1
	loop_count = 1
	with open(LOG_FILE_NAME, 'r') as f:
		
		session = alchemy.DBSession()
		dl = DbLoader()
		
		for line in f:
			
			try:
				
				if loop_count == LOG_EVERY_N: 
					print ("Reached line {0} - commit in progress ...".format(line_count))
					session.commit()
					loop_count = 0
					break # FIXME: only for debug
				
				t = dl.to_bulk(line)
				session.add(t)
				
				
				#~ if line.find('postfix/qmgr') > -1:
					#~ 
						#~ if line.find('removed') > -1:
							#~ t = dl.postfix_qmgr_removed(line)
							#~ session.add(t)
						#~ else:
							#~ t = dl.postfix_qmgr(line)
							#~ session.add(t)
				#~ 
				#~ if line.find('postfix/smtpd') > -1:
								#~ 
						#~ if line.find(': connect from') > -1:
							#~ t = dl.postfix_smtpd_connect(line)
							#~ session.add(t)
							#~ 
						#~ elif line.find(": disconnect from") > -1:
								#~ t = postfix_smtpd_disconnect(line)
								#~ session.add(t)
						#~ else:
							#~ pass
			
			except Exception as e:
				
				print ("ERROR while parsing line {0}:".format(line_count))
				t = dl.dump(line)
				session.add(t)
				
			
			line_count += 1
			loop_count += 1
