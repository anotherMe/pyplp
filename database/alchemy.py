#!/usr/bin/env python

DB_FILE_NAME = 'pyplp.db'

import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Boolean

Base = declarative_base()

class Bulk(Base):
	__tablename__ = 'bulk'
	
	"""	Table used to put all lines
	"""
	
	id = Column(Integer, primary_key=True)
	timestamp = Column(DateTime(timezone=False))
	host = Column(String(250))
	process_name = Column(String(50))
	process_id = Column(Integer)
	smtp_id = Column(String(10))
	#~ connect = Column(Boolean())
	stuff = Column(Text())
	
#~ class Dump(Base):
	#~ __tablename__ = 'dump'
	#~ 
	#~ """	Table used to put all lines we can't / wan't to parse
	#~ """
	#~ 
	#~ id = Column(Integer, primary_key=True)
	#~ timestamp = Column(DateTime(timezone=False))
	#~ host = Column(String(250))
	#~ process_name = Column(String(50))
	#~ process_id = Column(Integer)
	#~ code = Column(String(50))
	#~ stuff = Column(Text())


class BounceType(Base):
	__tablename__ = 'DICT_bouncetype'
	
	id = Column(Integer, primary_key=True)
	descr = Column(String(50))

class Bounced(Base):
	__tablename__ = 'bounced'
	
	id = Column(Integer, primary_key=True)
	timestamp = Column(DateTime(timezone=False))
	smtp_id = Column(String(250))
	mail_to = Column(String(250))
	relay = Column(String(250))
	conn_use = Column(Integer)
	delay = Column(String(250))
	delays = Column(String(250))
	dsn = Column(String(250))
	bounce_type = Column(Integer, ForeignKey('DICT_bouncetype.id'), nullable=False)
			

#~ class Disconnect(Base):
	#~ __tablename__ = 'disconnect'
#~ 
	#~ id = Column(Integer, primary_key=True)
	#~ timestamp = Column(DateTime(timezone=False))
	#~ host = Column(String(250))
	#~ process_name = Column(String(50))
	#~ process_id = Column(Integer)
	#~ connect_from = Column(String(100))
	#~ connect_from_IP = Column(String(50))
	#~ stuff = Column(Text())
	#~ 
#~ class Connect(Base):
	#~ __tablename__ = 'connect'
#~ 
	#~ id = Column(Integer, primary_key=True)
	#~ timestamp = Column(DateTime(timezone=False))
	#~ host = Column(String(250))
	#~ process_name = Column(String(50))
	#~ process_id = Column(Integer)
	#~ connect_from = Column(String(100))
	#~ connect_from_IP = Column(String(50))
	#~ stuff = Column(Text())
		#~ 
#~ 
#~ class Removed(Base):
	#~ __tablename__ = 'removed'
	#~ 
	#~ """	postfix/qmgr process removed records
	#~ """
	#~ 
	#~ id = Column(Integer, primary_key=True)
	#~ timestamp = Column(DateTime(timezone=False))
	#~ host = Column(String(250))
	#~ process_name = Column(String(50))
	#~ process_id = Column(Integer)
	#~ smtp_id = Column(String(250))
	#~ stuff = Column(Text())
	#~ 
#~ 
#~ class Qmgr(Base):
	#~ __tablename__ = 'qmgr'
	#~ 
	#~ """	postfix/qmgr process records
	#~ """
	#~ 
	#~ id = Column(Integer, primary_key=True)
	#~ timestamp = Column(DateTime(timezone=False))
	#~ host = Column(String(250))
	#~ process_name = Column(String(250))
	#~ process_id = Column(Integer)
	#~ smtp_id = Column(String(250))
	#~ message = Column(String(250))
	#~ message_long = Column(String(250))
	#~ mail_from = Column(String(250))
	#~ size = Column(Integer)
	#~ nrcpt = Column(Integer)
	#~ queue = Column(String(250))
#~ 
#~ class Smtpd(Base):
	#~ __tablename__ = 'smtpd'
	#~ 
	#~ """	postfix/smtpd process records
	#~ """
	#~ 
	#~ id = Column(Integer, primary_key=True)
	#~ timestamp = Column(DateTime(timezone=False))
	#~ host = Column(String(250))
	#~ process_name = Column(String(250))
	#~ process_id = Column(Integer)
	#~ smtp_id = Column(String(250))
	#~ message = Column(String(250))
	#~ message_long = Column(String(250))
	#~ mail_from = Column(String(250))
	#~ size = Column(Integer)
	#~ nrcpt = Column(Integer)
	#~ queue = Column(String(250))


engine = create_engine('sqlite:///' + DB_FILE_NAME)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


if __name__ == "__main__":

	if os.path.exists(DB_FILE_NAME):
		os.remove(DB_FILE_NAME)

	print("Creating schema on db file {0}".format(DB_FILE_NAME))
	Base.metadata.create_all(engine)
	session = DBSession()
	t = BounceType(descr='bounced')
	session.add(t)
	t = BounceType(descr='deferred')
	session.add(t)
	session.commit()
	

