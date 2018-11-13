import sqlite3
import json
import hashlib, os

class Customer(object):
    def __init__(self,email=None,password=None,id_=None):
        if id_ is None and email is not None and password is not None:
            self.status = self._login(email,password)
        else:
            self._email = email
            self.status = True

        self._email = ""
        if email is not None:
            self._email = email

        self._phoneno = 0
        
        self._name = ""
        self._address = ""
        self.db = sqlite3.connect('database.db')


        
    def _login(self,email, password):
        with sqlite3.connect('database.db') as con:
            try:
                cur=con.cursor()
                cur.execute('SELECT password from PASSENGER WHERE email=?',(email,))
                data=cur.fetchall()
                if(data==password):
                    return True
                else:
                    return False
            except:
                pass
                
    def _register(self,password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone):
        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO users (password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone)
                con.commit()

                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
   
        return msg