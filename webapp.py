import os
from flask import *
from flask import Flask,redirect,url_for,request,render_template
from flask import g
import sqlite3

app = Flask(__name__,template_folder="templates/html")

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="battlefield4",
#   database="footballmanagement"
# )
# print(mydb)
DATABASE = 'C://Users//suhas//Desktop//5th Sem//LabProject//Login_v11//Login_v11//airline_reservation.db'

@app.route('/')
def welcome():
    print("inside welcome in flask")
    return render_template('index.html')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/dbhandling/displayflights', methods = ['GET'])
def returnjson_file():
    for airplane in query_db('select * from airplane'):
        print(airplane) 

    return "<h1>HEllo world<h1>"

@app.route('/loginclick',methods=['GET','POST'])
def loginClick():
    print('inside login click')
    return render_template('dashboard.html')   

@app.route('/login',methods=['GET','POST'])
def login():
    print('inside login click')
    return render_template('dashboard.html') 

@app.route('/booking.html',methods=['GET','POST'])
def bookingpage():
    print('inside login click')
    return render_template('booking.html') 

@app.route('/cancel.html',methods=['GET','POST'])
def cancel():
    print('inside login click')
    return render_template ('cancel.html') 

@app.route('/searchforflights.html',methods=['GET','POST'])
def searchflight():
    print('inside login click')
    return render_template('searchforflights.html')

@app.route('/user',methods=['GET','POST'])
def userdisplay():
    print('inside login click')
    return render_template('user.html')

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    print('inside login click')
    return render_template('dashboard.html')

@app.route('/confirmbooking',methods=['GET','POST'])
def confirmClick():

    id1 = request.form['flightid']
    numticket = request.form['numticket']
    classbook = 'EPRICE'
    username = "Suhas"
    paymentstatus = "completed"

    print(id1,numticket,classbook,username,paymentstatus)


    # json_input  = request.get_json()
    with sqlite3.connect('airline_reservation.db') as con:
            try:
                cur = con.cursor()
                import pdb; #pdb.set_trace()
                cur.execute("INSERT INTO TICKET(FLIGHT,USERNAME,TIMEOFBOOKING,PAYMENTSTATUS,PRICE)VALUES(?,?,DATETIME('NOW'),?,())",( id1,username,paymentstatus))
                con.commit()

                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
            #con.close()
            print( msg)

    return render_template('payment.html')

  

if __name__ == '__main__': 

    app.run(debug = True)