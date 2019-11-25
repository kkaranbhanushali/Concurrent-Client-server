import threading
import socket
import sqlite3
import json
from datetime import datetime

db = sqlite3.connect('Bank.db',check_same_thread=False) 

cur=db.cursor()


cur.execute("DROP TABLE IF EXISTS piggybank")
cur.execute("CREATE TABLE IF NOT EXISTS piggybank(username TEXT,balance int,last_transaction int)")


cur.execute("DROP TABLE IF EXISTS statement")
cur.execute("CREATE TABLE IF NOT EXISTS statement(username TEXT,balance int,last_transaction int ,timestamp TEXT)")
db.commit()


class bankwork(threading.Thread):
    def __init__(self,soc,username):
        threading.Thread.__init__(self)
        self.soc=soc
        self.username=username
        self.balance=0
        self.lt=0


    def deposit(self,amount):
        if amount!=0:
            cur.execute("SELECT username from piggybank where username = ? ",(self.username,))
            l1=cur.fetchall()

            if len(l1)==0: #if empty then inserting default values and performing the 1st transaction

                cur.execute("INSERT into piggybank VALUES (?,?,?)",(self.username,self.balance,self.lt))
                db.commit()
                
                print("length of l1-->",len(l1))
                self.balance=self.balance+amount
                
                cur.execute("UPDATE piggybank SET balance = balance + ? , last_transaction = ? where username = ? ",(amount,amount,self.username))
                cur.execute("INSERT into statement VALUES (?,?,?,?)",(self.username,self.balance,amount,datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

                db.commit()


            else:
                cur.execute("SELECT balance from piggybank where username = ? ",(self.username,))
                
                l1=cur.fetchone()

                self.balance=l1[0]     # we are fetching only one account so only one acocunt we wil get so we wrote l1[0]
                self.balance=self.balance+amount
                cur.execute("UPDATE piggybank SET balance = balance + ? , last_transaction = ? where username = ? ",(amount,amount,self.username))
                cur.execute("INSERT into statement VALUES (?,?,?,?)",(self.username,self.balance,amount,datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                db.commit()

            str="{} deposited  successfully\n".format(amount)
            print("amount deposited  successfully\n")
            self.soc.send(str.encode())
        else:
            self.soc.send("amount less than zero\n".encode())


    def withdraw(self,amount):
        cur.execute("SELECT username from piggybank where username = ? ",(self.username,))
        l1=cur.fetchall() #fetching total names

        if len(l1)==0: #checking whether the usernames exists or does not exist
            cur.execute("INSERT into piggybank VALUES (?,?,?)",(self.username,self.balance,self.lt)) #inserting name and balance=0 , lt=0
            db.commit()

        cur.execute("SELECT balance from piggybank where username = ? ",(self.username,)) 
        l1=cur.fetchone() #fetching balance of account holder and storing in the list . it would be only one value
        a=int(l1[0])     #storing balance in a 
        print("value of l1-->",l1)
        print("value of a-->",a)

        if l1[0]>= amount:    #balance should always be greater than amount
            self.balance=a
            self.balance=self.balance-amount
            cur.execute("UPDATE piggybank SET balance = balance - ? , last_transaction = - ? where username = ? ",(amount,amount,self.username))
            cur.execute("INSERT into statement VALUES (?,?,-?,?)",(self.username,self.balance,amount,datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            db.commit()
            str="{} rs withdrawn successfully\n".format(amount)
            self.soc.send(str.encode())
        else:
            self.soc.send("insufficient balance\n".encode())


    def statement(self):

        cur.execute("SELECT username from piggybank where username = ? ",(self.username,))
        l1=cur.fetchall()
        
        if len(l1)==0: #inserting if account doesn't exist
            cur.execute("INSERT into piggybank VALUES (?,?,?)",(self.username,self.balance,self.lt))
            db.commit()
            self.soc.send("ZERO Transactions done \n".encode())
        else:
            cur.execute("SELECT balance,last_transaction from piggybank where username = ? ",(self.username,))
            l1=cur.fetchone()
            print(l1)
            
            cur.execute("SELECT balance,last_transaction,timestamp from statement where username = ? ",(self.username,))
            l1=cur.fetchall()
            
            listlen=len(l1) 
            sttring="\n"

            for i in range(listlen):   
                #json string
                res={
                    "balance":l1[i][0] , "Last_transaction":l1[i][1] , "Timestamp":l1[i][2]
                }
                
                sttring=sttring+ json.dumps(res) +"\n" #string concatenation to shift the next output to next line


            self.soc.send(sttring.encode())

            print("list looks like ->",l1)
            print("balance-->",self.balance)
            print("Last transaction-->",self.lt)
        
            
    def run(self):
        userinput=""
        while userinput!="q":
            userinput=self.soc.recv(1024).decode()
            if userinput=="d":
                amount=int(self.soc.recv(1024).decode())

                self.deposit(amount)

            elif userinput=="w":
                amount=int(self.soc.recv(1024).decode())

                self.withdraw(amount)

            elif userinput=="s":
                self.statement()
            elif userinput=="q":
                print("client left")

        self.soc.close()


        
    
    
ss=socket.socket()

ss.bind(("Localhost",8091))

ss.listen(5)

while True:
    s,add=ss.accept()
    print("connected to -->",add)
    username=s.recv(1024).decode()
    bankwork(s,username).start()


