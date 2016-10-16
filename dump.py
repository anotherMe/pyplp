
			if line.find('postfix/qmgr') > -1:
				
					if line.find('removed') > -1:
						t = parse_postfix_qmgr_removed(line)
						session.add(t)
					
					#~ elif line.find('skipped') > -1:
						#~ # TODO: parse lines like this one: Oct  9 11:08:06 mail03 postfix/qmgr[30290]: DA75823B95: skipped, still being delivered
						#~ pass
					#~ 
					#~ elif line.find('expired') > -1:
						#~ # TODO: parse lines like this one: Oct 12 16:52:33 mail03 postfix/qmgr[31995]: 8254822A68: from=<news@mail03.gas.it>, status=expired, returned to sender
						#~ pass
					#~ 
					#~ else:
						#~ t = parse_postfix_qmgr(line)
						#~ session.add(t)
			
			elif line.find('postfix/smtp') > -1:

				if line.find('status=bounced') > -1:
					t = parse_bounced(line)
					session.add(t)
			
			elif line.find('postfix/smtpd') > -1:
					
				if line.find(': connect from') > -1:
					t = parse_postfix_smtpd_connect(line)
					session.add(t)
					
				elif line.find(": disconnect from") > -1:
					t = parse_postfix_smtpd_disconnect(line)
					session.add(t)
						
			else:
				#~ t = parse_dump(line, "SKIPPED")
				#~ session.add(t)
				pass
