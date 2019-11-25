import socket
import json

cs = socket.socket()

cs.connect(("Localhost",8091))

username = input("Please enter your username-->")

cs.send(username.encode())


print("Welcome\n")

str="Type 'd' to deposit\n Type 'w' to withdraw\n Type 's' for statement\n Type 'q' to quit\n PLease enter your choice-->"
userinput=input(str).lower()

while userinput!="q":
    if userinput=="d":
        cs.send(userinput.encode())
        amount=input("please enter the amount to be deposited\n Enter here-->")
        cs.send(amount.encode())
        msg=cs.recv(1024).decode()
        print(msg)
    
    elif userinput=="w":
        cs.send(userinput.encode())
        amount=input("Please enter the amount to be withdrawn\n Enter here-->")
        cs.send(amount.encode())
        msg=cs.recv(1024).decode()
        print(msg)

    elif userinput=="s":
        cs.send(userinput.encode())

        msg=cs.recv(1024).decode()
        rmsg=msg.replace("{","")
        rmsg=rmsg.replace("}","\n")
        
        print(rmsg)

    else:
        print("Incorrect input\n")

    userinput=input(str).lower()

cs.send(userinput.encode())