import socket
import threading
import time
import sys, getopt
import string

name='Computer 1'		# -n <Name of current chatter> 
ipv6addr='::1'			# -a <ipv6 address to be used by this program> 
portno=11111			# -p <port number on which this program will receive chat msgs from others> 
ipv6party=['::1','::1']		# -d <ipv6 address of 2nd Chatter/Party>,<ipv6 address of 3rd Chatter/party> 
portparty=['12222','13333']	# -r <port number of 2rd Chatter/party>,<port number of 3rd Chatter/party>
oplist = ["-n","-a","-p","-d","-r"]
	

#to take the command line arguments
try:
	opts, args = getopt.getopt(sys.argv[1:],"n:a:p:d:r:",["name=","ipv6addr=","portno=","ipv6party=","portparty="])
except getopt.GetoptError: #incase of error 
	print 'ERROR, Please follow the following format : '
	print '\nasn1.py -n <Your Name> -a <Your ipv6 address to be used by this program>  -p <Your port number on which this program will receive chat msgs from others> -d <The ipv6 address of 2nd party>,<The ipv6 address of 3rd party> -r <port number of 2nd party>,<port number of 3rd party>'
  	sys.exit()

#assigning values to variables
for opt, arg in opts:
    	if opt not in(oplist):
		print 'ERROR, Please follow the following format: '
		print '\nasn1.py -n <Your Name> -a <Your ipv6 address to be used by this program>  -p <Your port number on which this program will receive chat msgs from others> -d <The ipv6 address of 2nd party>,<The ipv6 address of 3rd party> -r <port number of 2nd party>,<port number of 3rd party>'
     		sys.exit()

      	elif opt in ("-n", "--name"):
        	name = arg
      	elif opt in ("-a", "--ipv6addr"):
        	ipv6addr = arg
      	elif opt in ("-p", "--portno"):
        	portno = int(arg)
      	elif opt in ("-d", "--ipv6party"):
        	ipv6party = arg.split(',')
      	elif opt in ("-r", "--portparty"):
        	portparty = arg.split(',')
	
print '\n\t---------------------------------------------------'
print '\t\tWELCOME TO 3-PARTY IPv6 CHAT'	
print '\n\t---------------------------------------------------'
print '\t\tMy Name: ',name       			# <Name of current chatter> 
print '\t\tMy IPv6 Address: ',ipv6addr   		# <ipv6 address to be used by this program> 
print '\t\tMy port number: ',portno     		# <port number on which this program will receive chat msgs from others> 
print '\t\tIP address of Second Party:',ipv6party[0]	# <ipv6 address of 2nd chatter/party>
print '\t\tIP address of Third Party:',ipv6party[1]	# <ipv6 address of 3rd chatter/party> 
print '\t\tPort of First Party: ',portparty[0]		# <port number of 2nd chatter/party>
print '\t\tPort of Second Party: ',portparty[1]		# <port number of 3rd chatter/party>

print '\n\t---------------------------------------------------'
print '\n\t---------------------------------------------------'

#sender
def client():
	print "\n Lets Begin chatting, Enter your message or wait for one!!!" 
	while True: 	
		MESSAGE = raw_input()
		if(MESSAGE != 'end'): #while the user does not enter 'end' 
			send_addr1 = (ipv6party[0],int(portparty[0]),0,0)	#Set the address, and port number of the 2nd party to chat with
			send_addr2 = (ipv6party[1],int(portparty[1]),0,0)	#Set the address, and port number of the 3rd party to chat with
			sock.sendto(name+': '+MESSAGE, send_addr1) 		#Sending the message to the 2nd party
			sock.sendto(name+': '+MESSAGE, send_addr2)		#Sending the message to the 3rd party
		else:  #when the user enters 'end' we close the socket and stop sending messages
			sock.close()
			sys.exit(2)

#receiver
def server():
	time.sleep(1)
	while True:
		data, addr = sock.recvfrom(1024)	#buffer size is 1024 bytes
		print "Received message:", data 	#printing the message received

if __name__ == '__main__':				
	sock = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)	#creating the socket
	sock.bind(('',portno)) 					#binding the socket to OUR port number
	threading.Thread(target = server).start()		#starting the receiver thread			
	threading.Thread(target = client).start()		#starting the sender thread

