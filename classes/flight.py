import sqlite3
import json
from Transaction import *
from Order import *
import hashlib, os


class flight(Object):

	def insertflight(flightid,airplaneid,departure,arrival,d_time,a_time,a_date,d_date,ecap,bcap,eprice,bprice)
	with sqlite3.connect('database.db') as con
	try :
		cur=con.cursor()
		cur.execute('INSERT INTO FLIGHT VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(flightid,airplaneid,departure,d_date,arrival,a_time,d_date,a_date,bcap,ecap,bprice,eprice))
		con.commit()

		msg="added successfully"
	except:
		con.rollback()
		msg="error occured"
	con.close
	return msg