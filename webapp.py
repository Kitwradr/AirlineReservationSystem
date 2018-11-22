import os
from flask import *
from flask import Flask,redirect,url_for,request,render_template
from flask import g
import sqlite3
import pdb
from pymongo import MongoClient
import json

client = MongoClient()
db = client.airplaneReviews
collection = db.reviews

app = Flask(__name__,template_folder="templates/html")

user_id = 12

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="battlefield4",
#   database="footballmanagement"
# )
# print(mydb)
DATABASE = 'C://Users//suhas//Documents//GitHub//AirlineReservationSystem//airline_reservation.db'

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

@app.route('/postusername',methods=['POST'])
def postusername():

    session.username = request.form['username']
    print("session username = "+session.username)
    return session.username


@app.route('/login',methods=['GET','POST'])
def login():
    print('inside login click')
    return render_template('dashboard.html') 

@app.route('/bookflight',methods=['GET','POST'])
def bookingpage():
    flightid = request.args.get('flightid')
    print('inside bookflight flightid = '+str(flightid))
    session.flightid = flightid
    if(flightid is None):
        return render_template('booking.html')
    else:
        return render_template('booking.html',flightid = flightid)
  
    


@app.route('/cancel.html',methods=['GET','POST'])
def cancel():
    print('inside login click')
    return render_template ('cancel.html') 


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

@app.route('/dashboard.html',methods=['GET','POST'])
def dashboard1():
    print('inside login click')
    return render_template('dashboard.html')

@app.route('/maps.html',methods=['GET','POST'])
def mapsdisplay():
    print('inside login click')
    return render_template('maps.html')

@app.route('/registration.html',methods=['GET','POST'])
def registration():
    return render_template('registration.html')

@app.route('/registrationclick',methods=['GET','POST'])
def registrationclick():
  
    name = request.form['name']
    username = request.form['username']
    bdate = request.form['birthday']
    gender = request.form['gender']
    email = request.form['email']
    phone = request.form['phone']
    print(name,username,bdate,gender,email,phone)

    with sqlite3.connect('airline_reservation.db') as con:
            try:
                cur = con.cursor()
                 #pdb.set_trace()
                cur.execute("INSERT INTO PASSENGER (password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",("alberquerqe",email,name," ","2nd stage","Vijayanagar","560040","Bangalore","Karnataka","India",phone))
                con.commit()

                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
            #con.close()
            print( msg)

    return render_template('index.html')

@app.route('/loginadmin',methods=['GET','POST'])
def displayadminview():

    return render_template('admin.html')

@app.route('/retrieveReviews',methods = ['POST','GET'])
def retrieveReviews():
    json_input = request.get_json()

    flight_id = json_input["flight_id"]

    print(flight_id)

    res = ""
    for review in collection.find({'flightid':flight_id}):
        res+="<tr>"
        
        res+="<td>"+str(review["rating"])+"</td>"
        res+="<td>"+str(review["review"])+"</td>"
        res+="</tr>"

    print(json.dumps({"status":200,"data":res}))

    return json.dumps({"status":200,"data":res})

@app.route('/generateticket',methods = ['GET','POST'])
def generateticket():
    ticketID = 0
    ticketDetails = ""

    return render_template('ticket.html')

@app.route('/submitreview',methods=['GET','POST'])
def submmitreview():
    data = {}
    rating = request.form['rating']
    review = request.form['reviewparagraph']

    print(rating,review)

    data['userID'] = user_id
    data['ticketID'] = "23"
    data['review'] = review
    data['flightid'] = "45"
    data['rating'] = rating

    

    json_data = json.dumps(data)
    print(collection.insert_one(data).inserted_id)

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
                 #pdb.set_trace()
                cur.execute("INSERT INTO TICKET(FLIGHT,USERNAME,TIMEOFBOOKING,PAYMENTSTATUS,PRICE)VALUES(?,?,DATETIME('NOW'),?,?*(SELECT EPRICE FROM FLIGHT WHERE FLIGHTID=? ))",( id1,username,paymentstatus,numticket,id1))
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