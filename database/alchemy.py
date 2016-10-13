#!/usr/bin/python3

DB_FILE_NAME = 'sqlalchemy_example.db'

import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text

Base = declarative_base()

class Temp(Base):
	__tablename__ = 'temporary'
	
	"""	Temporary table used to make aggregation analysis on log data.
	"""
	
	id = Column(Integer, primary_key=True)
	timestamp = Column(DateTime(timezone=False))
	host = Column(String(250))
	process_name = Column(String(50))
	process_id = Column(Integer)
	smtp_id = Column(String(20))
	message = Column(Text())

class Disconnect(Base):
	__tablename__ = 'disconnect'

	id = Column(Integer, primary_key=True)
	timestamp = Column(DateTime(timezone=False))
	host = Column(String(250))
	process_name = Column(String(50))
	process_id = Column(Integer)
	connect_from = Column(String(100))
	connect_from_IP = Column(String(50))
	stuff = Column(Text())
	
class Connect(Base):
	__tablename__ = 'connect'

	id = Column(Integer, primary_key=True)
	timestamp = Column(DateTime(timezone=False))
	host = Column(String(250))
	process_name = Column(String(50))
	process_id = Column(Integer)
	connect_from = Column(String(100))
	connect_from_IP = Column(String(50))
	stuff = Column(Text())
		

class Removed(Base):
	__tablename__ = 'removed'
	
	"""	postfix/qmgr process removed records
	"""
	
	id = Column(Integer, primary_key=True)
	timestamp = Column(DateTime(timezone=False))
	host = Column(String(250))
	process_name = Column(String(50))
	process_id = Column(Integer)
	smtp_id = Column(String(250))
	stuff = Column(Text())
	

class Qmgr(Base):
	__tablename__ = 'qmgr'
	
	"""	postfix/qmgr process records
	"""
	
	id = Column(Integer, primary_key=True)
	timestamp = Column(DateTime(timezone=False))
	host = Column(String(250))
	process_name = Column(String(250))
	process_id = Column(Integer)
	smtp_id = Column(String(250))
	message = Column(String(250))
	message_long = Column(String(250))
	mail_from = Column(String(250))
	size = Column(Integer)
	nrcpt = Column(Integer)
	queue = Column(String(250))

class Smtpd(Base):
	__tablename__ = 'smtpd'
	
	"""	postfix/smtpd process records
	"""
	
	id = Column(Integer, primary_key=True)
	timestamp = Column(DateTime(timezone=False))
	host = Column(String(250))
	process_name = Column(String(250))
	process_id = Column(Integer)
	smtp_id = Column(String(250))
	message = Column(String(250))
	message_long = Column(String(250))
	mail_from = Column(String(250))
	size = Column(Integer)
	nrcpt = Column(Integer)
	queue = Column(String(250))


engine = create_engine('sqlite:///' + DB_FILE_NAME)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


if __name__ == "__main__":

	if os.path.exists(DB_FILE_NAME):
		os.remove(DB_FILE_NAME)

	Base.metadata.create_all(engine)

