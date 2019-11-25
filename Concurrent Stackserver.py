import socket
import threading
import sqlite3
from datetime import datetime


db = sqlite3.connect('Stacklist.db',check_same_thread=False)

cur=db.cursor()

cur.execute("DROP TABLE IF EXISTS stacklist")
cur.execute("CREATE TABLE IF NOT EXISTS stacklist(list TEXT,object_id TEXT,timestamp TIMESTAMP)")
db.commit()


class stackwork(threading.Thread):

    def __init__(self,soc,name):
        threading.Thread.__init__(self)
        self.soc=soc
        self.username=name

        



    def push(self,value):



        
        cur.execute("SELECT list FROM stacklist WHERE object_id = ? ",(self.username,))

        # #fetching list from stacklist which give us total number of rows of the table

        l1=cur.fetchall()

        if len(l1)<10:
        
        

            print("value of r--> ",value)

            #insert query
            cur.execute("INSERT INTO stacklist VALUES (?,?,?)",(value,self.username,datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

            db.commit()
            sendstr="value of {} pushed successfully\n".format(value)
            self.soc.send(sendstr.encode())
            print("pushed value\n")

        else:
            self.soc.send("stack full please delete some items \n".encode())
        



    def popvalue(self):

        
        
        cur.execute("SELECT list FROM stacklist WHERE object_id = ? ",(self.username,))

        #fetching list from stacklist which will give us total number of rows of the table

        l1=cur.fetchall()



        print("lenght of l1 is -->",len(l1))

        if len(l1)==0:
            self.soc.send("Nothing to pop\n""Please Enter something\n".encode())
        else:
            name=self.username

            cur.execute("SELECT list,timestamp from stacklist where object_id = ? order by timestamp desc limit 1",(name,))
            
            #to cross verify the deleted item

            l1= cur.fetchall()

            l=l1.pop() #to get the deleted value

            print("value of l is -->",l)
            print("value to be deleted -->",l) #it will give the deleted item
            
            
            popquer="DELETE FROM stacklist WHERE object_id = '{}' and timestamp = (SELECT timestamp from stacklist where object_id = '{}' order by timestamp desc limit 1)".format(self.username,self.username)

            cur.execute(popquer) #pop query 

            db.commit()
            
            sendstr="Popped {} successfully".format(l)
            self.soc.send(sendstr.encode())
            print("popped")
        

    def printvalue(self):
        
        cur.execute("SELECT list,timestamp FROM stacklist WHERE object_id = (?) ",(self.username,))
        #fetching list , timestamp and storing in list

        l1=(cur.fetchall())

        if len(l1)==0:

            self.soc.send("Nothing to print\n""Please Enter something\n".encode())
        else:
            #converting list to string because only string can passed through socket
            stl=str(l1).strip('[]')
            self.soc.send(stl.encode())


    

    def run(self):  

        userinput=""
        while userinput!="e":
            userinput=self.soc.recv(1024).decode()
            if userinput=="pu":
                a=self.soc.recv(1024).decode()
                self.push(a)
            
            elif userinput=="po":
                self.popvalue()

            elif userinput=="pr":
                self.printvalue()

            elif userinput=="d":
                cur.execute("DELETE FROM stacklist WHERE object_id = (?) ",(self.username,))
                db.commit()


            elif userinput=="e":
                print("client left")
        
        # cur.execute("DELETE FROM stacklist WHERE object_id = (?) ",(self.username,))
        db.commit()
        self.soc.close()










#server socket creation
ss=socket.socket()

ss.bind(("Localhost",8090))

ss.listen(5)





#main loop waiting for the client
while True:
    s,add=ss.accept()
    print("Connected to ",add)
    cname=s.recv(1024).decode()
    #creation of new thread to perform task

    stackwork(s,cname).start()
