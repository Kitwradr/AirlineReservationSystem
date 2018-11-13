import sqlite3
import json
from Transaction import *
from Order import *
import hashlib, os

class ticket(Object):

	def getTicket(username,flightid,no_of_tickets,pstatus,grade)
	 with sqlite3.connect('database.db') as con
	  try:
	     cur=con.connect()
	     if(pstatus=="COMPLETED")
	     		cur.execute('INSERT INTO TICKET VALUES (?,?,DATETIME('NOW'),PAYMENTSTATUS,?* SELECT grade from flight where flightid = ? )',(flightid,username,no_of_tickets,grade,flightid,))
	     		con.commit()
	     		msg="added successfully"
	     
	     else
	      msg="payment not completed"

	  except
	  	con.rollback()
	  	msg="error occured"
	  con.close()

	  return msg