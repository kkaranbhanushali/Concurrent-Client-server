import socket

cs = socket.socket()

cs.connect(("Localhost",8090))


username=input("Hello user \n Please Enter your name-->")

cs.send(username.encode())

userinput =""

print("Welcome to stack server\n")

str="Please enter your choice\n Type 'po' to pop\n Type 'pu' to push\n Type 'pr' to print\n Type 'd' to delete all data \n Type 'e' to end\n Enter here-->"

userinput=input(str).lower()
    
while userinput!="e":
    if userinput=="po":
        cs.send(userinput.encode())
        mess=cs.recv(1024).decode()
        print("message:-->",mess)


    elif userinput=="pu":
        
        cs.send(userinput.encode())
        a=input("please enter the value to be pushed-->")
        cs.send(a.encode())

        mess=cs.recv(1024).decode()
        print(mess)

        # print("pushing {} succesfull".format(a))


    elif userinput=="pr":
        cs.send(userinput.encode())
        mess=cs.recv(1024).decode()
        print("Stack-->",mess)

    elif userinput=="d":
        cs.send(userinput.encode())
        print("Cleared all data from the stack\n")
    else :
        print("Incorrect input\n")

    userinput=input(str)

cs.send(userinput.encode())
    
    












        # a=int(a)
        # if type(a)==int:
        #     cs.send(userinput.encode())
        # # print("{}".format(a))
        #     cs.send(a.encode())
        #     print("pushing {} succesfull".format(a))
        # else:
        #     print("Only integers are allowed")