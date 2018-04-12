import socket
import argparse
import pickle
import threading

parser = argparse.ArgumentParser()
#username as input
parser.add_argument('-u', type = str, help = 'input username', action = 'store')
#IP address that the server is connected to as input
parser.add_argument('-sip', type = str, help = 'input the server\'s IP ', action = 'store')
#Port to be connected to as input
parser.add_argument('-sp', type = int, help = 'input the port number', action = 'store')
args = parser.parse_args()
####print args

#values taken as input assigned to variables
UN = args.u
SIP = args.sip
UDP_PORT = args.sp

#lists for storing data from the pickle file
names =[]
addr = []
port = []

cl = []
cla = []
clp = []

ru = []
rip = []
rpn = []

#function to send messages to another client
def sendmsg(msg):
    #removing the command from the original message
    msg = msg[5:]
    #extracting receiver's name
    rec = msg.partition(' ')[0]
    ####print rec
    #to send data to the receiver
    msg = msg[(len(rec)+1):]
    ####print msg
    #getting the place of user item in 'names' list
    i = names.index(rec)
    #making variables for receiver's ip-address and port
    RIP = addr[i]
    R_PORT = port[i]
    BUFFER_SIZE = 1024
    while msg:
        sentbytes = sc.sendto(msg[:BUFFER_SIZE], (RIP, R_PORT))
        msg = msg[sentbytes:]

#function to receive messages from another client
def recvmsg():
    while True:
        #to receive data
        data, adr = sc.recvfrom(1024)
        try:
            with open('clients.pkl', 'rb') as f:
                while True:
                    ru.append(pickle.load(f))
                    rip.append(pickle.load(f))
                    rpn.append(pickle.load(f))
        except EOFError:
            pass
        if not data:
            chat()
            rt.exit()
        #extracting sender's username
        #we find the index of the given address in the list & extract the username
        j = rpn.index(adr[1])
        SUN = ru[j]
        print '<-- <From ' + str(adr[0]) + ' : ' + str(adr[1]) + ' : ' + SUN + '>: ' + data+'\n+>'
   
#basic function
def chat():
    while(1):
        #starting the message receiving thread
        rt = threading.Thread(target = recvmsg)
        rt.start()

        msg = raw_input('+>')

        #extracting the command
        cmd = msg.partition(' ')[0]
        
        if cmd == "list":
            try:
                with open('clients.pkl', 'rb') as f:
                    while True:
                        cl.append(pickle.load(f))
                        cla.append(pickle.load(f))
                        clp.append(pickle.load(f))
            except EOFError:
                pass
            print '<-- Signed In Users:'+' '.join(str(p) for p in cl)
            cl[:] = []

        elif cmd == "send":
            try:
                with open('clients.pkl', 'rb') as f:
                    while True:
                        names.append(pickle.load(f))
                        addr.append(pickle.load(f))
                        port.append(pickle.load(f))
            except EOFError:
                pass
    
            try:
                #starting the message sending thread
                st = threading.Thread(target = sendmsg(msg))
                st.start()
                ####sendmsg(msg) 
            except socket.error, emsg:
                print 'Error: ' + str(emsg)

        else:
            print 'Incorrect command/message'
        
#socket creation
if __name__ == "__main__":
    try:
        sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sc.sendto(UN, (SIP, UDP_PORT))
    except socket.error, msg:
        print 'Socket creation failed'+msg
    #####sc.bind((SIP, UDP_PORT))
    #caalling the actual chat funtion to perform tasks
    chat()
    #closing connection
    sc.close