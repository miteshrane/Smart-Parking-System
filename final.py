import mysql.connector as mysql
import serial 
import time
from datetime import datetime


db = mysql.connect(host = "localhost",user = "root",password="root",database = "database")          #connection with the database.
device = 'COM4'         #port being used.
try:
  print("Trying...",device)
  arduino = serial.Serial(device, 9600)         #read the data from arduino connected to the com port specified in 'device'.

except: 
  print("Failed to connect on",device)
while True:
    time.sleep(1)
    try:
        data = arduino.readline()   #Read the tag from arduino and store it in a variable called data.
        
        try:
            
            cursor = db.cursor()    #cursor class executes queries on the connected database.
            query = "SELECT timestamp from rfid where rfid_tag = %s"        #selects timestamp from the row in database where the stored rfid tag equals the rfid that is read.
            cursor.execute(query,(data.split()[0],))        #passes the read rfid tag to the above statement in the database.
            result = cursor.fetchall()      #stores the timestamp in result.
            
            encoding = 'utf-8'
            res = str(data.split()[1], encoding)    #type converting from bytes to string, in order to check a valid/invalid tag.
        
            if res == 'valid':
                print('Valid Tag\n')
                if result[0][0]:
                    print('Exiting')            #enters this block if the value stored in 'result' is not null, which means the rfid already has an entry timestamp and the vehicle is exiting.
                    query = "update rfid set timestamp = %s where rfid_tag = %s"        #updates the timestamp from the row in database where the stored  rfid tag equals the read rfid tag to 0.
                    cursor.execute(query,(0,data.split()[0],))          #executes the above query statement in the database.
                    db.commit()
                    entry_time = result[0][0]       #Storing the entry time.
                    exit_time = datetime.now()      #storing the exit time.
                    print('Vehicle tag number',int(data.split()[0]))
                    print('Entry time',entry_time)    
                    print('Exit time',exit_time)
                    diff = (exit_time - entry_time)     #compute the duration of the parking.
                    print('Duration in parking=',diff)
                    print('Parking fare = $',round(diff.total_seconds(), 2))     #parking fare rounded off to 2 decimal places.
                    print('****************')
                else:
                    print('Entering')           #enters this  block if the value in 'result' is null, which means the rfid is tapped for the first time and the vehicle is entering.
                    print('Vehicle tag number',int(data.split()[0]))
                    query = "update rfid set timestamp = %s where rfid_tag = %s"        #updates the timestamp from the row in database where the stored  rfid tag equals the read rfid tag to current time.
                    timestamp = datetime.now()          #stores the current time of the machine as entry time of the rfid 
                    cursor.execute(query,(timestamp,data.split()[0],))          #executes the above query statement in the database.
                    db.commit()
                    print('Entry time',timestamp)
                    print('############')
            else:
                print('Please use valid tag\n')
        except:
            print("")
        finally:
            cursor.close()
    except:
        print("Processing")