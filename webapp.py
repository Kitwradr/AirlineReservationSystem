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
app.secret_key = 'random string'

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


@app.route('/loginClick',methods=['POST'])
def loginClick():
    
    email = request.form['email']
    
    password = request.form['password']

    print(email,password)
    with sqlite3.connect('airline_reservation.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT password from PASSENGER WHERE email=?',(email,))
        data=cur.fetchall()
        print("password = "+str(data[0][0]))
        if(data[0][0]==password):
            session['username'] = request.form['email']
            print("session username = "+session['username'])
            return "success"
        else:
            return "Failure" 


@app.route('/login',methods=['GET','POST'])
def login():
    print('inside login click')
    return render_template('dashboard.html') 

@app.route('/bookflight',methods=['GET','POST'])
def bookingpage():
    flightid = request.args.get('flightid')
    print('inside bookflight flightid = '+str(flightid))
    session['flightid'] = '\"'+str(flightid)+'\"'
    if(flightid is None):
        return render_template('booking.html')
    else:
        return render_template('booking.html',flightid = flightid)
  
    


@app.route('/cancel.html',methods=['GET','POST'])
def cancel():
  
    return render_template ('cancel.html') 


@app.route('/calculatecost',methods=['GET','POST'])
def calculatecost():
    print('inside calculate cost')
    print("received flight id"+request.form['flight_id'])
    flightid = request.form['flight_id']
    numtickets = request.form['numtickets']
    classBook = request.form['classBook']
    username=session['username']
    with sqlite3.connect('airline_reservation.db') as conn:
        #pdb.set_trace()
        cur = conn.cursor()
        sql = "Select "+numtickets+"*eprice From flight Where flightid="+flightid
        print(sql)
        cur.execute(sql)
        costdb = cur.fetchone()
        print(costdb)

        cur.execute("""select email
                from passenger 
                where username in(
                SELECT USERNAME  
                FROM TICKET 
                GROUP BY USERNAME 
                ORDER BY COUNT(TICKETID) DESC Limit 5)""")       
        disc=cur.fetchall()
        print("disc = "+str(disc))
        for row in disc :
            if row[0] == username :
                discount=0.1
        temp=costdb[0]-(costdb[0]*discount)
        temp = round(temp)
    print(str(temp),str(costdb[0]-temp))

    return json.dumps({'data1':str(temp),'data2':str(costdb[0]-temp)})




@app.route('/searchforflights.html',methods=['GET','POST'])
def searchflight():

    source = request.form['source']
    destination = request.form['destination']
    date = request.form['date']
  
    if 'username' not in session:
        session['username'] = '\"suhashe\"'
    with sqlite3.connect('airline_reservation.db') as con:
            try:
                cur = con.cursor()
                pdb.set_trace()
                sql_statement = """SELECT FLIGHTID
                                    FROM FLIGHT AS F
                                    WHERE FLIGHTID IN(
                                        ( SELECT F.FLIGHTID
                                            FROM FLIGHT AS F, AIRPORT AS AR
                                            WHERE AR.AIRPORTCODE=F.ARRIVAL AND AR.CITY="?"
                                            
                                            INTERSECT
                                            
                                            SELECT F.FLIGHTID
                                            FROM FLIGHT AS F , AIRPORT AS AR
                                            WHERE AR.AIRPORTCODE=F.DEPARTURE AND AR.CITY="?")
                                    ) AND F.D_DATE="?"; """
                print(sql_statement)
                
                cur.execute(sql_statement,(source,destination,date))

                flights = cur.fetchall()

                print(flights)
                

                msg = "Registered Successfully"
            except:
               
                msg = "Error occured"
            #con.close()
            print(msg)

    return "The ticket was successfully cancelled"


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
  
    return render_template('dashboard.html')

@app.route('/dashboard.html',methods=['GET','POST'])
def dashboard1():
 
    return render_template('dashboard.html')


@app.route('/registration.html',methods=['GET','POST'])
def registration():
    return render_template('registration.html')

@app.route('/registrationClick',methods=['POST'])
def registrationclick():
    print(request.form)

    name = request.form['name']
    username = request.form['username']
    bdate = request.form['birthday']
    gender = request.form['gender']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    print(name,username,bdate,gender,email,phone,password)

    with sqlite3.connect('airline_reservation.db') as con:
            try:
                cur = con.cursor()
                sqlQuery = "Insert into passenger values ('"+str(username)+"','"+str(name)+"','"+str(email)+"','"+str(phone)+"','"+str(gender)+"','"+str(bdate)+"','"+str(password)+"')"
                print(sqlQuery)
                cur.execute(sqlQuery)
                con.commit()

                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
            #con.close()
            print( msg)

    return "You were registered sucessfully"

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
    ticket_details = []
    with sqlite3.connect('airline_reservation.db') as con:
        try:
            cur = con.cursor()
        
            sql_statement = """SELECT DAIR.CITY,AAIR.CITY,T.PRICE,AP.COMPANY,F.D_DATE,F.FLIGHTID,T.TICKETID
                                FROM AIRPORT AS DAIR,AIRPORT AS AAIR, FLIGHT AS F, TICKET AS T,AIRPLANE AS AP
                                WHERE F.FLIGHTID=T.FLIGHT AND DAIR.AIRPORTCODE=F.DEPARTURE AND AAIR.AIRPORTCODE=F.ARRIVAL AND T.USERNAME="""+'"'+session['username']+'"'+" AND AP.AIRPLANEID=F.AIRPLANEID AND F.FLIGHTID="+session['flightid']
            print(sql_statement)
            cur.execute(sql_statement)
            tickets = cur.fetchone()

            
      

            ticket_details.append(tickets[0]+"  ")
            ticket_details.append(tickets[1]+"  ")
            ticket_details.append(tickets[2])
            ticket_details.append(tickets[3])
            ticket_details.append(tickets[4])
            ticket_details.append(str(tickets[5]))
            ticket_details.append(str(tickets[6]))
            
            print("ticket_details = "+str(ticket_details))

            msg = "Registered Successfully"
        except:
            msg = "Error occured"
        print( msg)
        
    return render_template('ticket.html',ticket_details = ticket_details)

@app.route('/submitreview',methods=['GET','POST'])
def submitreview():
    data = {}
    rating = request.form['rating']
    review = request.form['reviewparagraph']

    print(rating,review)

    data['userID'] = user_id
    data['ticketID'] = session['ticket_id']
    data['review'] = review
    data['flightid'] = session['flightid']
    data['rating'] = rating

    print(data,collection.insert_one(data).inserted_id)

    return render_template('dashboard.html')

@app.route('/retrieveTickets',methods=['GET','POST'])
def retrieveTicketsinfo():

    if 'username' not in session:
        session['username'] = '\"Suhas HE\"'
    with sqlite3.connect('airline_reservation.db') as con:
            try:
                cur = con.cursor()
                #pdb.set_trace()
                sql_statement = """SELECT DAIR.CITY,AAIR.CITY,T.PRICE,AP.COMPANY,F.D_DATE,T.TICKETID,F.FLIGHTID
                                FROM AIRPORT AS DAIR,AIRPORT AS AAIR, FLIGHT AS F, TICKET AS T,AIRPLANE AS AP
                                WHERE F.FLIGHTID=T.FLIGHT AND DAIR.AIRPORTCODE=F.DEPARTURE AND AAIR.AIRPORTCODE=F.ARRIVAL AND F.A_DATE<=DATE('now') AND T.USERNAME="""+'"'+session['username']+'"'+" AND AP.AIRPLANEID=F.AIRPLANEID"""
                print(sql_statement)
                
                cur.execute(sql_statement)
                tickets = cur.fetchall()
                if len(tickets[0])>3:
                    session['ticket_id'] = tickets[0][5]
                    session['flightid'] = tickets[0][6]
                print(tickets)

                msg = "Registered Successfully"
            except:
               
                msg = "Error occured"
            #con.close()
            print( msg)
            print(json.dumps(tickets))

    return json.dumps(tickets)

@app.route('/retrieveTicketsforCancel',methods=['GET','POST'])
def retrieveTicketsforCancel():

    if 'username' not in session:
        session['username'] = '\"suhashe\"'
    with sqlite3.connect('airline_reservation.db') as con:
            try:
                cur = con.cursor()
                #pdb.set_trace()
                sql_statement = """SELECT DAIR.CITY,AAIR.CITY,T.PRICE,AP.COMPANY,F.D_DATE,T.TICKETID
                                FROM AIRPORT AS DAIR,AIRPORT AS AAIR, FLIGHT AS F, TICKET AS T,AIRPLANE AS AP
                                WHERE T.PRICE>0 AND F.D_DATE>=DATE('NOW') AND F.FLIGHTID=T.FLIGHT AND DAIR.AIRPORTCODE=F.DEPARTURE AND AAIR.AIRPORTCODE=F.ARRIVAL AND T.USERNAME="""+'"'+session['username']+'"'+" AND AP.AIRPLANEID=F.AIRPLANEID"""
                print(sql_statement)
                cur.execute(sql_statement)
                tickets = cur.fetchall()
                session['ticket_id'] = tickets[0][5]
                print(session)
                print(tickets)

                msg = "Registered Successfully"
            except:
               
                msg = "Error occured"
            #con.close()
            print( msg)
            print(json.dumps(tickets))

    return render_template('cancel.html',tickets = tickets)


@app.route('/confirmbooking',methods=['GET','POST'])
def confirmClick():
    
    flightid = request.form['flightid']
    session['flightid'] = '\"'+str(flightid)+'\"'
    numticket = request.form['numticket']
    classbook = 'EPRICE'
    print("session = "+str(session))
    if 'username' not in session:
        session['username'] = '\"Suhas HE\"'

    paymentstatus = "completed"

    print(flightid,numticket,classbook,session['username'],paymentstatus)


    # json_input  = request.get_json()
    with sqlite3.connect('airline_reservation.db') as con:
            try:
                cur = con.cursor()
                 #pdb.set_trace()
                cur.execute("INSERT INTO TICKET(FLIGHT,USERNAME,TIMEOFBOOKING,PAYMENTSTATUS,PRICE)VALUES(?,?,DATETIME('NOW'),?,?*(SELECT EPRICE FROM FLIGHT WHERE FLIGHTID=? ))",( flightid,session['username'],paymentstatus,numticket,flightid))
                con.commit()

                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
            #con.close()
            print( msg)

    return render_template('payment.html')

@app.route('/cancelTicket',methods=['GET','POST'])
def cancelTicket():

    if 'username' not in session:
        session['username'] = '\"suhashe\"'
    with sqlite3.connect('airline_reservation.db') as con:
            try:
                cur = con.cursor()
                pdb.set_trace()
                sql_statement = """UPDATE TICKET
                                SET PRICE = -20 WHERE
                                TICKETID = ?"""
                print(sql_statement)
                
                cur.execute(sql_statement,(session['ticket_id'],))
                

                msg = "Registered Successfully"
            except:
               
                msg = "Error occured"
            #con.close()
            print(msg)

    return "The ticket was successfully cancelled"

    
  

if __name__ == '__main__': 

    app.run(debug = True)