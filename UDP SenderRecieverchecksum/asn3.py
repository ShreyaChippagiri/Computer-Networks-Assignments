#UDP Server program - Server implements the SR receiver, and Client implements the SR sender. 

import sys, getopt
import string
from socket import *
import random 
from datetime import datetime

def main(argv):	
	serverPort=12345
	cack=30
	cpack=20
	npack=10
	window=3

	try:
		opts, args = getopt.getopt(argv,"hp:s:r:N:w:",["portno=","ackperc=","pakperc=","numpak=","winsize="])
	except getopt.GetoptError:
		print '\n'
		print "Error in command line arguements"
		print "Please give the command line arguements in the following format: " 
		print 'asn3.py -p <server port number> -s <corruption percent of acks sent> -r <corruption percent of packets sent> -N <total number of packets sent> -w <window size>'
      		sys.exit()

	for opt, arg in opts:
      		if (opt == '-h'):#In case user asks for help
			print '\n'
			print "Error in command line arguements"
			print "Please give the command line arguements in the following format: " 
      			print "asn3.py -p<server port number> -s<corruption percent of acks sent> -r<corruption percent of packets sent> -N<total number of packets sent> -w<window size>"
      			sys.exit()

		if (len(sys.argv)<11):
			print '\n'
			print "Error in command line arguements"
			print "Please give the command line arguements in the following format: " 
		      	print 'asn3.py -p<server port number> -s<corruption percent of acks sent> -r<corruption percent of packets sent> -N<total number of packets sent> -w<window size>'
			sys.exit()
      		elif opt in ("-p", "--portno"):
         		serverPort = int(arg)
      		elif opt in ("-s", "--ackper"):
         		cack = int(arg)
     		elif opt in ("-r", "--pakper"):
         		cpack = int(arg)
      		elif opt in ("-N", "--numpak"):
         		npack = int(arg)
			if(npack<10):
				print "The number of packets cannot be less than 10! Please re-run the program and enter the values!!! "
				sys.exit()
      		elif opt in ("-w", "--winsize"):
         		window = int(arg)
	print '\n'
	print '\tServer Port : ',serverPort
   	print '\tCorruption percent of acks sent : ',cack,'%'
   	print '\tCorruption percent of packets sent : ',cpack,'%'
   	print '\tTotal number of packets : ',npack
   	print '\tWindow size : ', window
	print '\n'
		
	base = 0
	end = window
#-------------------------------------------------corruption of packets by the reciever-------------------------	 
	#GENERATING THE LIST OF THE PACKETS THAT WE CORRUPT BEFORE ACCEPTING
	ncp = ((npack*cpack))/100 #ncp = number of corrupted packets (we corrupt before storing in our list)
	print cpack,'% of ',npack,':',ncp,'packets to be corrupted!!'
	corruptpacketnolist = [] #contains sequence numbers of corrupted packets RANDOMLY GENERATED 		
	for i in range(0,ncp):
		n = random.randint(0,npack-1)
		while n in corruptpacketnolist:
			n = random.randint(0,npack-1)
		corruptpacketnolist.append(n)
	print '-----------------------------------------------------------------'
	print 'Further Calculations/Predictions : '
	print "Seq no of packets that will be corrupted : ",corruptpacketnolist #random packets that we are corrupting
	

	#GENERATING THE LIST OF THE ACKS THAT WE CORRUPT BEFORE SENDING

	corruptackslist = [] #contains the random seqno of a packet whose ack will be corrupted/not sent
	remainingpack = npack-ncp
	corruptacks = (cack*remainingpack)/100
	ackedpacketsnolist2=[] #random seq numbers of non corrupted packets (created statically)
	mom=[]
	for mm in range(npack):
		if mm not in corruptpacketnolist:
			ackedpacketsnolist2.append(mm)
	
	for i in range(corruptacks):
		ca = random.randint(0,(len(ackedpacketsnolist2))-1) #ca is the random index generated of the ackedpackets list to access a particular seqno
		while ca in mom:
			ca = random.randint(0,(len(ackedpacketsnolist2))-1)
		corruptackslist.append(ackedpacketsnolist2[ca]) #contains the random seqno of a packet whose ack will be corrupted/not sent
		mom.append(ca)
	print "Seq no of acks of received packets that will be corrupted : ", corruptackslist
	print '-----------------------------------------------------------------'

	#STARTING THE CONNECTION
	serverName = ''
	serverSocket = socket(AF_INET, SOCK_DGRAM)
	serverSocket.bind(('', serverPort))
	print "\nSR RECEIVER or UDP Server ready to receive data"
	message, clientAddr = serverSocket.recvfrom(2048)
  	print "Servent sent: ", message
   	
	#SENDING THE WINDOW SIZE AND NUMBER OF PACKETS TO THE SENDER, so that it initiates the sending process
	serverSocket.sendto(str(window), clientAddr)
	serverSocket.sendto(str(npack), clientAddr)

	receivedpacket = [] #the list that contains packets successfully received by the receiver
	corruptedlist = [] #the corrupted packets (seqno, checksum, data) 
	ackedpacketsnolist = [] #sequence number of the packets that are ack-ed


	#FUNCTION THAT SENDS THE ACK 
	def sendingack(message):
		splitpacket2 = message.split(',')
		#print "splitpacket - 2", splitpacket2
		sq = int(splitpacket2[0]) 
		checksumbit2 = int(splitpacket2[1])
		ackmsg = ""	
		if (sq not in (corruptackslist)):
			ackmsg = ackmsg + splitpacket2[0] + ',' + splitpacket2[1]
			print "Ack sent : ", ackmsg, ' at ', str(datetime.now()),' (This will NOT GET CORRUPTED)'
			serverSocket.sendto(ackmsg, clientAddr)
			return
		else:
			ackmsg = ackmsg + splitpacket2[0] + ',' + '0'
			print "Ack sent : ", ackmsg, ' at ', str(datetime.now()),' (This will GET CORRUPTED)'
			serverSocket.sendto(ackmsg, clientAddr)
			return
			
	

	#RECEIVING PACKETS FROM THE SENDER
	while 1:
 		message, clientAddr = serverSocket.recvfrom(2048)
		print '-----------------------------------------------------------------'
    		print "\nServer Sent this : ", message
		splitpacket=[]
		splitpacket = message.split(',')
		#print "splitpacket", splitpacket
		sno = int(splitpacket[0]) 
		# to determine whether to corrupt the packet or not
		#Generating a list of packets that have to be corrupted as per the given command line arguements
		emptymsg=""		
		if sno in corruptpacketnolist:
			splitpacket[1] = '0' #changing the checksum value
			print "PACKET CORRUPTED : checkum changed of seq number-", sno
			corruptedlist.append(splitpacket) #list of corrupted packets
			receivedpacket.append(emptymsg) #appending an empty message in place of the corrupted packet in the received list
			corruptpacketnolist.remove(sno) #to remove the sequence number of the packet that is corrupted once, so that we receive it next time.
		else:
			if message in receivedpacket:
				print 'Packet number : ',sno,' has been received "AGAIN" as a result of retransmission! At the time : ',str(datetime.now())
				sendingack(message)
			else:
				print 'Packet number : ', sno, ' received at ', str(datetime.now())
				receivedpacket.append(message) #the list of not-corrupted packets
				ackedpacketsnolist.append(sno) #the sequence numbers of the non-corrupted packets
				sendingack(message)
				#if sno in range(windsize['base'], windsize['end']):
				while base in ackedpacketsnolist:
					base = base+1
					end = end+1
					print '\nMoving the window - WINDOW: [',base,',',end,']'	

		print "\nCorrupted List so far : ", corruptedlist	
		print "Packets the receiver has : ", receivedpacket
	print '-----------------------------------------------------------------'

if __name__ == "__main__":
	main(sys.argv[1:])	
